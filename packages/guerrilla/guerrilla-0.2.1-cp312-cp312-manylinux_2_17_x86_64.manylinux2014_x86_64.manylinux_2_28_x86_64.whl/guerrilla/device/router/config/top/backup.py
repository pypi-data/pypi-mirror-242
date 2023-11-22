from guerrilla.device.router.config import BaseConfig
from guerrilla.device.router.command import Commands

class AutoBackup(BaseConfig):
    def enable_config(self):
        """
        Enables automatic backup of the configuration.
        
        Examples:
            >>> device.config.auto_backup.enable_config()
        """
        cmd: str = Commands.CONFIG.AUTOBACKUP.ENABLE_CONFIG
        self._execute_config_command(cmd, success_message="Automatic backup of configuration enabled.")

    def disable_config(self):
        """
        Disables automatic backup of the configuration.
        
        Examples:
            >>> device.config.auto_backup.disable_config()
        """
        cmd = Commands.CONFIG.AUTOBACKUP.DISABLE_CONFIG
        self._execute_config_command(cmd, success_message="Automatic backup of configuration disabled.")

    def enable(self):
        """
        Enables hardware interface for auto-backup.
        
        Examples:
            >>> device.config.auto_backup.enable()
        """
        cmd:str = Commands.CONFIG.AUTOBACKUP.ENANBLE_AUTOBACKUP
        self._execute_config_command(cmd, success_message="Hardware interface for auto-backup enabled.")

    def disable(self):
        """
        Disables hardware interface for auto-backup.
        
        Examples:
            >>> device.config.auto_backup.disable()
        """
        cmd:str = Commands.CONFIG.AUTOBACKUP.DISABLE_AUTOBACKUP
        self._execute_config_command(cmd, success_message="Hardware interface for auto-backup disabled.")

    def enable_auto_load_config(self):
        """
        Enables auto-load of configuration on bootup.
        
        Examples:
            >>> device.config.auto_backup.enable_auto_load_config()
        """
        cmd: str = Commands.CONFIG.AUTOBACKUP.DISABLE_AUTO_LOAD_CONFIG
        self._execute_config_command(cmd, success_message="Auto-load of configuration on bootup enabled.")

    def disable_auto_load_config(self):
        """
        Disables auto-load of configuration on bootup.
        
        Examples:
            >>> device.config.auto_backup.disable_auto_load_config()
        """
        cmd: str = Commands.CONFIG.AUTOBACKUP.DISABLE_AUTO_LOAD_CONFIG
        self._execute_config_command(cmd, success_message="Auto-load of configuration on bootup disabled.")