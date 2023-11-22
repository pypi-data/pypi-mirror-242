from guerrilla.device.router.config import BaseConfig
from guerrilla.device.router.command import Commands

class ConfigFirmwareCheck(BaseConfig):
    
    def enalbe(self):
        """
        Enables firmware check.
        
        Examples:
            >>> device.config.config_fwr_ver_check.enalbe()
        """
        cmd: str = Commands.CONFIG.FIRMWARECHECK.ENABLE
        self._execute_config_command(cmd, success_message="Firmware check enabled.")
        
    def disable(self):
        """
        Disables firmware check.
        
        Examples:
            >>> device.config.config_fwr_ver_check.disable()
        """
        cmd: str = Commands.CONFIG.FIRMWARECHECK.DISABLE
        self._execute_config_command(cmd, success_message="Firmware check disabled.")