from guerrilla.device.router.config import BaseConfig
from guerrilla.device.router.command import Commands

class IpPingResponse(BaseConfig):
    
    def enable(self):
        """
        Enable the ping response for WAN interface.
        
        Example:
            >>> device.config.ip_ping_response.enable()
        """
        cmd: str = Commands.CONFIG.IP.PING.ENABLE
        self._execute_config_command(cmd, success_message="Ping response enabled.")
        
    def disable(self):
        """
        Disable the ping response for WAN interface.
        
        Example:
            >>> device.config.ip_ping_response.disable()
        """
        cmd: str = Commands.CONFIG.IP.PING.DISABLE
        self._execute_config_command(cmd, success_message="Ping response disabled.")