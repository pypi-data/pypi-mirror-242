from guerrilla.device.router.config import BaseConfig
from guerrilla.device.router.command import Commands

class Hostname(BaseConfig):
    
    def set_hostname(self, hostname):
        """
        Sets the hostname of the router.

        Args:
            hostname (str): The new hostname to set. max 30 characters
            
        Examples:
            >>> device.config.hostname.set_hostname('New York')
        """
        cmd = Commands.CONFIG.HOSTNAME.SET(hostname)
        self._execute_config_command(cmd, f"Hostname set to {hostname}")
    
    def reset_hostname(self):
        """
        Resets the hostname of the router to the default.
        
        Examples:
            >>> device.config.hostname.reset_hostname()
        """
        cmd: str = Commands.CONFIG.HOSTNAME.RESET
        self._execute_config_command(cmd, "Hostname reset to default")