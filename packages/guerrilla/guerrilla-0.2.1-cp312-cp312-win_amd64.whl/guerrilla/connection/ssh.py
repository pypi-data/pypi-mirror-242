from dataclasses import dataclass, field
from typing import override, Optional, Callable, Union, List
import paramiko
from guerrilla.connection.session import BaseSession
from guerrilla.logging import logger
from guerrilla.connection.channel import SSHChannel
from guerrilla.utils.exception import SSHAuthenticationError
from guerrilla.connection.response import Response
import re

@dataclass
class SSHSession(BaseSession):
    host: str = ""
    username: str = ""
    password: str = ""
    port: int = 22
    client: paramiko.SSHClient = field(default_factory=paramiko.SSHClient, init=False)
    channel: SSHChannel = field(init=False)

    def _is_alive(self) -> bool:
        """
        Checks if the SSH channel is still active.

        Returns:
        --------
        bool
            True if the channel is active, False otherwise.
        """
        transport = self.client.get_transport()
        return transport and transport.is_active()

    def _establish_connection(self):
        """
        Tries to connect to the remote server using SSH.
        """
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        logger.info(f"Created {self.name}'s SSH session to {self.host}:{self.port}")
        try:
            self.client.connect(
                hostname=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
            )
        except paramiko.AuthenticationException as e:
            raise SSHAuthenticationError(e, self.host, self.port)
        except Exception:
            logger.error(f"Could not connect to {self.host}:{self.port}")
            raise ConnectionError("Could not connect to remote server")
        logger.success(f"Connected to {self.username} {self.host}:{self.port}")

        remote_conn = self.client.invoke_shell(width=511, height=1000)
        self.channel = SSHChannel(remote_conn)

    def disconnect(self):
        """
        Closes the SSH connection.
        """
        try:
            self.client.close()
            logger.info(f"Closed connection to {self.host}:{self.port}")
        except Exception:
            logger.error(f"Error when closing connection to {self.host}:{self.port}")
            raise ConnectionError("Could not close connection")
        
    



LINUX_PROMPT_PRI = "$"
LINUX_PROMPT_ALT = "#"
LINUX_PROMPT_ROOT = "#"
@dataclass
class LinuxSSHSession(SSHSession):
    prompt_pattern: str = (
        rf"[{re.escape(LINUX_PROMPT_PRI)}{re.escape(LINUX_PROMPT_ALT)}]"
    )
    
    @override
    def run(
        self,
        command: str, 
        expect_string: str = None, 
        read_timeout: int = 30, 
        error_detector: Optional[Callable[[str], bool]] = None, 
        extend_error: Union[str, List[str], None] = None
        ) -> tuple[str , str , bool]:
        expect_string = expect_string or r'\$|#'
        output, raw_output, failed = super().run(command, 
                                                        expect_string=expect_string, 
                                                        read_timeout=read_timeout,
                                                        error_detector=error_detector,
                                                        extend_error=extend_error
                                                        )
        return output, raw_output, failed
    
    @override
    def session_preparation(self):
        """Prepare the session after the connection has been established."""
        self.ansi_escape_codes = True
        self._test_channel_read(pattern=self.prompt_pattern)
        self.set_base_prompt()
        
    @override
    def find_prompt(
        self, delay_factor: float = 1.0, pattern: Optional[str] = None
    ) -> str:
        if pattern is None:
            pattern = self.prompt_pattern
        return super().find_prompt(delay_factor=delay_factor, pattern=pattern)
    
    @override
    def set_base_prompt(
        self,
        pri_prompt_terminator: str = LINUX_PROMPT_PRI,
        alt_prompt_terminator: str = LINUX_PROMPT_ALT,
        delay_factor: float = 1.0,
        pattern: Optional[str] = None,
    ) -> str:
        """Determine base prompt."""
        if pattern is None:
            pattern = self.prompt_pattern
        return super().set_base_prompt(
            pri_prompt_terminator=pri_prompt_terminator,
            alt_prompt_terminator=alt_prompt_terminator,
            delay_factor=delay_factor,
            pattern=pattern,
        )
    
    def login_as_root(self, root_password: str) -> None:
        """
        Login as root user.

        Parameters:
        -----------
        root_password: str
            The root password.
        """
        self.run("su", expect_string="Password:")
        self.run_timing(root_password)
        self.set_base_prompt()
        logger.success(f"Logged in as root user on {self.host}:{self.port}")