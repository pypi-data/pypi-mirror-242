from dataclasses import dataclass
from typing import Union
from guerrilla.device.base import BaseDevice
from contextlib import contextmanager
from guerrilla.utils.error import GuerrillaSettingError
from typing import List

@dataclass
class BaseConfig():
    _device: Union[None, BaseDevice] = None
    
    def _get_in(self):
        self._back_to_main()
        self._get_in_to_config_mode()
        self._get_in_target_mode()
        self._device.session.set_base_prompt()
        
    def _back_to_main(self):
        self._device._back_to_main()
        
    def _get_in_to_config_mode(self):
        self._device.run('configure', expect_string=r"\(config.*\)#")
        
        
    def _get_in_target_mode(self):
        pass

    @contextmanager
    def setting_config(self, save: bool = False):
        self._get_in()  
        should_save = True  
        try:
            yield
        except Exception: 
            should_save = False  
        finally:
            if should_save and save:
                self._device.save()
            else:
                self._back_to_main()
    
    def _execute_config_command(self, command: str, success_message: str, expect_string: str = None, extend_error: str | List[str] | None = None):
        with self.setting_config():
            response = self._device.run(command, expect_string=expect_string, extend_error=extend_error)
            if not response.failed :
                self._device.logger.success(success_message)
            else:
                self._device.logger.error(f"Command failed: {command}")
                raise GuerrillaSettingError(f"Command execution failed: {command}")

