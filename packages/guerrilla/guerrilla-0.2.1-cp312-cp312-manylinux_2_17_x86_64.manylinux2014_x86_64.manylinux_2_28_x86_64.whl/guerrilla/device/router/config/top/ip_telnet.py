from guerrilla.device.router.config import BaseConfig
from guerrilla.device.router.command import Commands

class IpTelnet(BaseConfig):
    def enable(self):
        """
        Enables the telnet service on the router.
        
        Example:
            >>> device.config.ip_telnet.enable()
        """
        cmd: str = Commands.CONFIG.IP.TELNET.ENABLE
        self._execute_config_command(cmd, success_message="Telnet service enabled.")
        
    def disable(self):
        """
        Disables the telnet service on the router.
        
        Example:
            >>> device.config.ip_telnet.disable()
        """
        cmd: str = Commands.CONFIG.IP.TELNET.DISABLE
        self._execute_config_command(cmd, success_message="Telnet service disabled.")
        
    def reset_max_login_users(self):
        """
        Resets the maximum number of login users.
        
        Example:
            >>> device.config.ip_telnet.reset_max_login_users()
        """
        cmd: str = Commands.CONFIG.IP.TELNET.RESET_MAX_LOGIN_USERS
        self._execute_config_command(cmd, success_message="Maximum number of login users reset.")
        
    def set_port(self, port: int):
        """
        Sets the telnet service port.
        
        Example:
            >>> device.config.ip_telnet.set_port(23)
        """
        cmd: str = Commands.CONFIG.IP.TELNET.SET_PORT(port)
        self._execute_config_command(cmd, success_message=f"Telnet service port set to {port}.")
        
    
    def set_max_login_users(self, max_login_users: int):
        """
        Sets the maximum number of login users.
        
        Example:
            >>> device.config.ip_telnet.set_max_login_users(5)
        """
        cmd: str = Commands.CONFIG.IP.TELNET.SET_MAX_LOGIN_USERS(max_login_users) # BUG
        self._execute_config_command(cmd, success_message=f"Maximum number of login users set to {max_login_users}.")