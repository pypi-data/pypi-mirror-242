from guerrilla.device.router.config import BaseConfig
from guerrilla.device.router.command import Commands

class PasswordPolicy(BaseConfig):
    
    def set_length(self, length: int):
        """
        Sets the minimum length for user passwords.

        Args:
            length (int): The minimum number of characters for the password. Minimum is 4, maximum is 16.
        
        Example:
            >>> device.config.password_policy.set_length(8)
        """
        cmd: str = Commands.CONFIG.PASSWORDPOLICY.SET_LENGTH(length)
        self._execute_config_command(cmd, success_message=f"Password policy minimum length set to {length}.")

    def reset_length(self):
        """
        Resets the password policy to the default minimum length.
        
        Example:
            >>> device.config.password_policy.reset_length()
        """
        cmd: str = Commands.CONFIG.PASSWORDPOLICY.RESET_LENGTH
        self._execute_config_command(cmd, success_message="Password policy minimum length reset to default.")

    def enable_complexity(self):
        """
        Enables the password complexity requirements.
        
        Example:
            >>> device.config.password_policy.enable_complexity()
        """
        cmd: str = Commands.CONFIG.PASSWORDPOLICY.ENABLE_COMPLEXITY
        self._execute_config_command(cmd, success_message="Password policy complexity enabled.")
        
    def disable_complexity(self):
        """
        Disables the password complexity requirements.
        
        Example:
            >>> device.config.password_policy.disable_complexity()
        """
        cmd: str = Commands.CONFIG.PASSWORDPOLICY.DISABLE_COMPLEXITY
        self._execute_config_command(cmd, success_message="Password policy complexity disabled.")
    
    def set_complexity(self, complexity_elements: str):
        """
        Sets the password complexity requirements.

        Args:
            complexity_elements (list): A list of complexity requirements to include ['digit', 'alphabet', 'special-characters'].
        
        Examples:
            >>> device.config.password_policy.set_complexity('digit')
            >>> device.config.password_policy.set_complexity('alphabet')
            >>> device.config.password_policy.set_complexity('special-characters')
        """
        cmd: str = Commands.CONFIG.PASSWORDPOLICY.SET_COMPLEXITY(complexity_elements)
        self._execute_config_command(cmd, success_message=f"Password policy {complexity_elements} complexity set.")

    def reset_complexity(self, complexity_elements: str):
        """
        Resets the password complexity requirements to default or specified elements.

        Args:
            complexity_elements (list, optional): A list of complexity requirements to reset. If None, resets all.
        
        Examples:
            >>> device.config.password_policy.reset_complexity('digit')
            >>> device.config.password_policy.reset_complexity('alphabet')
            >>> device.config.password_policy.reset_complexity('special-characters')
        """
        cmd: str = Commands.CONFIG.PASSWORDPOLICY.RESET_COMPLEXITY(complexity_elements)
        self._execute_config_command(cmd, success_message=f"Password policy {complexity_elements} complexity reset to default.")
    
    def set_max_life_time(self, maxlife_time: int):
        """
        Sets the maximum number of days a password can be used before it must be changed.

        Args:
            maxlife_time (int): The maximum number of days a password can be used. Minimum is 0, maximum is 365.
        
        Example:
            >>> device.config.password_policy.set_max_life_time(90)
        """
        cmd: str = Commands.CONFIG.PASSWORDPOLICY.SET_MAXLIFE_TIME(maxlife_time)
        self._execute_config_command(cmd, success_message=f"Password policy maxlife time set to {maxlife_time} days.")