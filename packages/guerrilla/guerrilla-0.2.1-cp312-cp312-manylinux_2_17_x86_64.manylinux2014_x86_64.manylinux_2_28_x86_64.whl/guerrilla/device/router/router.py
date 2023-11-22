from guerrilla.device.base import BaseDevice
from dataclasses import dataclass
import re
from typing import override, Optional
from guerrilla.device.router.config import Config
import time
from typing import Union, List
from guerrilla.device.router.mixin import ShowMixin, ReloadMixin, CopyMixin



@dataclass
class Router(BaseDevice, ShowMixin, ReloadMixin, CopyMixin):
    @override
    def connect(self):
        super().connect()
        self.disable_paging()
        self.config = Config(self)

    def disable_paging(
        self,
        command: str = "terminal length 0",
        cmd_verify: bool = False,
        pattern: Optional[str] = None,
    ) -> str:
        """Disable paging default to a CLI method.

        :param command: Device command to disable pagination of output

        :param delay_factor: Deprecated in Netmiko 4.x. Will be eliminated in Netmiko 5.

        :param cmd_verify: Verify command echo before proceeding (default: True).

        :param pattern: Pattern to terminate reading of channel
        """
        command = self.session.normalize_cmd(command)
        self.session.write_channel(command)
        # Make sure you read until you detect the command echo (avoid getting out of sync)
        if cmd_verify:
            output = self.session.read_until_pattern(
                pattern=re.escape(command.strip()), read_timeout=20
            )
        elif pattern:
            output = self.session.read_until_pattern(pattern=pattern, read_timeout=20)
        else:
            output = self.session.read_until_prompt()
        self.logger.info("Disable Paging Default")
        return output

    def _error_detector(self, output: str, extend_error: Union[str, List[str], None] = None) -> bool:
        if extend_error is None:
            extend_error = []
        elif isinstance(extend_error, str):
            extend_error = [extend_error]

        # Predefined patterns to match lines that start with ^ or %
        predefined_patterns = [r'\^(.*)', r'%(.*)']
        error_list = predefined_patterns + extend_error

        for error_pattern in error_list:
            match = re.search(error_pattern, output, re.M | re.I)
            if match:
                if error_pattern in predefined_patterns:
                    # This will capture the message after ^ or % and log it as a warning.
                    error_message = match.group(1)
                else:
                    # For other patterns, log the whole match.
                    error_message = match.group(0)
                self.logger.error(f"Error detected: {error_message}")
                return True

        return False

    @override
    def run(
        self, command: str, expect_string: str = None, extend_error: Union[str, List[str], None] = None, read_timeout: int = 30) -> str | None:
        response = super().run(command, 
                            expect_string=expect_string, 
                            read_timeout=read_timeout, 
                            error_detector=self._error_detector, 
                            extend_error=extend_error
                            )

        return response

    def check_config_mode(
        self, check_string: str = r"\(config.*\)#", pattern: str = "", force_regex: bool = True
    ) -> bool:
        """Checks if the device is in configuration mode or not.

        :param check_string: Identification of configuration mode from the device
        :type check_string: str

        :param pattern: Pattern to terminate reading of channel
        :type pattern: str

        :param force_regex: Use regular expression pattern to find check_string in output
        :type force_regex: bool

        """
        self.session.write_channel(self.session.RETURN)
        # You can encounter an issue here (on router name changes) prefer delay-based solution
        if not pattern:
            output = self.session.read_channel_timing(read_timeout=10.0)
        else:
            output = self.session.read_until_pattern(pattern=pattern)

        if force_regex:
            return bool(re.search(check_string, output))
        else:
            return check_string in output
        
    def config_mode(
        self, config_command: str = "", pattern: str = r"\(config.*\)#", re_flags: int = 0, cmd_verify: bool = True
    ) -> str:
        """Enter into config_mode.

        :param config_command: Configuration command to send to the device
        :type config_command: str

        :param pattern: Pattern to terminate reading of channel
        :type pattern: str

        :param re_flags: Regular expression flags
        :type re_flags: RegexFlag
        """
        output = ""
        if not self.check_config_mode():
            self.session.write_channel(self.session.normalize_cmd(config_command))
            # Make sure you read until you detect the command echo (avoid getting out of sync)
            if cmd_verify:
                output += self.session.read_until_pattern(
                    pattern=re.escape(config_command.strip())
                )
            if pattern:
                output += self.session.read_until_pattern(pattern=pattern, re_flags=re_flags)
            else:
                output += self.session.read_until_prompt(read_entire_line=True)
            if not self.check_config_mode():
                raise ValueError("Failed to enter configuration mode.")
        return output
    
    def exit_config_mode(self, exit_config: str = "exit", pattern: str = r"#.*", cmd_verify: bool = False, check: bool = False) -> str:
        """Exit from configuration mode.

        :param exit_config: Command to exit configuration mode
        :type exit_config: str

        :param pattern: Pattern to terminate reading of channel
        :type pattern: str
        """
        output = ""
        if self.check_config_mode():
            self.session.write_channel(self.session.normalize_cmd(exit_config))
            # Make sure you read until you detect the command echo (avoid getting out of sync)
            if cmd_verify is not False:
                output += self.session.read_until_pattern(
                    pattern=re.escape(exit_config.strip())
                )
            if pattern:
                output += self.session.read_until_pattern(pattern=pattern)
            else:
                output += self.session.read_until_prompt(read_entire_line=True)
            if check:
                if self.check_config_mode():
                    raise ValueError("Failed to exit configuration mode")
        self.logger.debug(f"exit_config_mode: {output}")
        return output
    
    def save(self):
        """
        Save the current configuration and return to the main menu.
        """
        self._back_to_main()
        self.run('save')
        
    def _back_to_main(self):
        """ Attempt to go back to the main menu, expect string is self.original_prompt """
        current_prompt = self.find_prompt()[:-1]
        end_time = time.time() + 5
        if current_prompt == self.session.original_prompt:
            self.logger.debug("Already in main menu")
            return
        else:
            while current_prompt != self.session.original_prompt and time.time() < end_time:
                self.logger.debug("current_prompt", current_prompt)
                self.logger.debug("original_prompt", self.session.original_prompt)
                self.session.write_channel('exit')
                time.sleep(0.2)
                current_prompt = self.find_prompt()[:-1]