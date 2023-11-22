from dataclasses import dataclass
from guerrilla.device.router.command import Commands

@dataclass
class CopyMixin:
    """
    This class provides methods to upload firmware, export and import configuration files
    to and from a device using various transfer methods such as TFTP, USB, SCP and SFTP.
    """
    
    error_extend = ["Configuration Upload Fail!", "Config file import failed.", "Input error", "No USB Device"]

    def _validate_transfer_details(self, transfer_method, ip, cfg_path_name, account, password, is_firmware=False):
        """
        Validates the transfer details such as transfer method, IP, configuration path name, account and password.
        Raises ValueError if any of the details are invalid.
        """
        method: str = transfer_method.lower()
        if is_firmware and method == 'usb':
            self.logger.error("USB method is not supported for firmware upload.")
            
        valid_methods = ['tftp', 'usb', 'scp', 'sftp']
        if method not in valid_methods:
            self.logger.warning(f"Invalid transfer method. Must be one of {valid_methods}.")

        if method in ['scp', 'sftp'] and (not account or not password):
            self.logger.warning("Account and password must be provided for SCP/SFTP.")

        if method == 'tftp' and (not ip or not cfg_path_name):
            self.logger.warning("IP and configuration path name must be provided for TFTP.")


    def upload_firmware(self, transfer_method: str, ip: str = '', filename: str = '', account: str = '', password: str = '') -> str:
        """
        Uploads firmware to the device using the specified transfer method.
        
        Examples:
            >>> device.upload_firmware('tftp', '192.168.127.3', 'firmware.rom')
            >>> device.upload_firmware('scp', '192.168.127.3', 'firmware.rom', 'admin', 'admin')
            >>> device.upload_firmware('sftp', '192.168.127.3', 'firmware.rom', 'admin', 'admin')
            >>> device.upload_firmware('usb', filename='firmware.rom')
        """
        self._validate_transfer_details(transfer_method, ip, filename, account, password, is_firmware=True)
        command: str = Commands.CONFIG.COPY(transfer_method, ip, filename, account, password, "device-firmware")
        response = self.run(command, 
                            expect_string="Checking transfer:Firmware Upgrade OK! Restart the device.", 
                            extend_error=self.error_extend ,
                            read_timeout=120
                            )
        if not response.failed:
            from yaspin import yaspin
            import time
            
            self.disconnect()
            with yaspin(text="Restarting...").shark as sp:
                time.sleep(30)
                sp.ok("✅ ")
            self.connect()
            self.logger.success(f"Upfrade firmware to {filename}.")
        return response

    def export_config(self, transfer_method: str, ip: str = '', cfg_path_name: str = '', account: str = '', password: str = ''):
        """
        Exports the configuration file from the device using the specified transfer method.
        
        Examples:
            >>> device.export_config('tftp', '192.168.127.3', 'default.ini')
            >>> device.export_config('scp', '192.168.127.3', 'default.ini', 'admin', 'admin')
            >>> device.export_config('sftp', '192.168.127.3', 'default.ini', 'admin', 'admin')
            >>> device.export_config('usb', cfg_path_name='default.ini')
        """
        self._validate_transfer_details(transfer_method, ip, cfg_path_name, account, password)
        command: str = Commands.CONFIG.EXPORT(transfer_method, ip, cfg_path_name, account, password)
        response = self.run(command, extend_error=self.error_extend)
        if not response.failed:
            self.logger.success(f"Exported configuration to {cfg_path_name}.")
        return response

    def import_config(self, transfer_method: str, ip: str = '', cfg_path_name: str = '', account: str = '', password: str = ''):
        """
        Imports the configuration file to the device using the specified transfer method.
        
        Examples:
            >>> device.import_config('tftp', '192.168.127.3', 'default.ini')
            >>> device.import_config('scp', '192.168.127.3', 'default.ini', 'admin', 'admin')
            >>> device.import_config('sftp', '192.168.127.3', 'default.ini', 'admin', 'admin')
            >>> device.import_config('usb', cfg_path_name='default.ini')
        """
        self._validate_transfer_details(transfer_method, ip, cfg_path_name, account, password)
        command: str = Commands.CONFIG.COPY(transfer_method, ip, cfg_path_name, account, password, "config-file")
        response = self.run(command, 
                            expect_string="Config file import successfully.",
                            extend_error=self.error_extend)
        if not response.failed:
            self.logger.success(f"Imported configuration from {cfg_path_name}.")
            self.connect()
        return response
