from guerrilla.device.router.config import BaseConfig
from guerrilla.device.router.command import Commands

class IpHttpServer(BaseConfig):
    
    def enable_http(self):
        """
        Enables the HTTP service on the router.
        
        Example:
            >>> device.config.ip_http_server.enable_http()
        """
        cmd: str = Commands.CONFIG.IP.HTTPSERVER.ENABLE
        self._execute_config_command(cmd, success_message="HTTP service enabled.")
        
    def disable_http(self):
        """
        Disables the HTTP service on the router.
        
        Example:
            >>> device.config.ip_http_server.disable_http()
        """
        cmd: str = Commands.CONFIG.IP.HTTPSERVER.DISABLE
        self._execute_config_command(cmd, success_message="HTTP service disabled.")
        
    def enable_https(self):
        """
        Enables the HTTPS service on the router.
        
        Example:
            >>> device.config.ip_http_server.enable_https()
        """
        cmd: str = Commands.CONFIG.IP.HTTPSERVER.ENABLE_HTTPS
        self._execute_config_command(cmd, success_message="HTTPS service enabled.")
        
    def disable_https(self):
        """
        Disables the HTTPS service on the router.
        
        Example:
            >>> device.config.ip_http_server.disable_https()
        """
        cmd: str = Commands.CONFIG.IP.HTTPSERVER.DISABLE_HTTPS
        self._execute_config_command(cmd, success_message="HTTPS service disabled.")
        
    def reset_max_login_users(self):
        """
        Resets the maximum number of login users.
        
        Example:
            >>> device.config.ip_http_server.reset_max_login_users()
        """
        cmd: str = Commands.CONFIG.IP.HTTPSERVER.RESET_MAX_LOGIN_USERS
        self._execute_config_command(cmd, success_message="Maximum number of login users reset.")
    
    def set_http_port(self, port: int):
        """
        Sets the HTTP service port.
        
        Args:
            port (int): The port number to set.
            
        Example:
            >>> device.config.ip_http_server.set_http_port(8080)
        """
        cmd: str = Commands.CONFIG.IP.HTTPSERVER.SET_HTTP_PORT(port)
        self._execute_config_command(cmd, success_message=f"HTTP service port set to {port}.")
    
    
    def set_https_port(self, port: int):
        """
        Sets the HTTPS service port.
        
        Args:
            port (int): The port number to set.
            
        Example:
            >>> device.config.ip_http_server.set_https_port(8443)
        """
        cmd: str = Commands.CONFIG.IP.HTTPSERVER.SET_HTTPS_PORT(port)
        self._execute_config_command(cmd, success_message=f"HTTPS service port set to {port}.")
        
    
    def set_max_login_users(self, max_login_users: int):
        """
        Sets the maximum number of login users.
        
        Args:
            max_login_users (int): The maximum number of login users to set.
            
        Example:
            >>> device.config.ip_http_server.set_max_login_users(10)
        """
        extend_error = [f'Maximum Login Users For HTTP+HTTPS "{max_login_users}" should be in range of 1 to 10.'] # BUG
        cmd: str = Commands.CONFIG.IP.HTTPSERVER.SET_MAX_LOGIN_USERS(max_login_users)
        self._execute_config_command(cmd, success_message=f"Maximum number of login users set to {max_login_users}.", extend_error=extend_error)