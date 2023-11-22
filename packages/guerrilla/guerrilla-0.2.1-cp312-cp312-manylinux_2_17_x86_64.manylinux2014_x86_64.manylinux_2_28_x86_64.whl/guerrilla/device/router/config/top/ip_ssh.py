from guerrilla.device.router.config import BaseConfig
from guerrilla.device.router.command import Commands

class IpSSH(BaseConfig):
    def enable(self):
        """
        Enables the SSH service on the router.
        
        Example:
            >>> device.config.ip_ssh.enable()
        """
        cmd: str = Commands.CONFIG.IP.SSH.ENABLE
        self._execute_config_command(cmd, success_message="SSH service enabled.")

    def set_port(self, port: int):
        """
        Sets the port number for the SSH service.

        Args:
            port (int): The port number for the SSH service.
            
        Example:
            >>> device.config.ip_ssh.set_port(22)
        """
        cmd: str = Commands.CONFIG.IP.SSH.SET_PORT(port)
        self._execute_config_command(cmd, success_message=f"SSH port set to {port}.")

    def disable(self):
        """
        Disables the SSH service on the router.
        
        Example:
            >>> device.config.ip_ssh.disable()
        """
        cmd: str = Commands.CONFIG.IP.SSH.DISABLE
        self._execute_config_command(cmd, success_message="SSH service disabled.")