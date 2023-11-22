from guerrilla.device.router.config import BaseConfig
from guerrilla.device.router.command import Commands

class User(BaseConfig):
    
    def add_user(self, username: str, password: str, privilege: int = 1):
        """
        Adds a new user with the specified username, password, and privilege level.

        Args:
            username (str): The username for the user. Max 30 characters, case-sensitive, no whitespace.
            password (str): The password for the user. Min 4 to max 16 characters, case-sensitive.
            privilege (int): The privilege level for the user (1 to 4).
            
        Examples:
            >>> device.config.user.add_user('testuser', 'testpassword', privilege=1)
        """
        command: str = Commands.CONFIG.USER.ADD(username, password, privilege)
        self._execute_config_command(command, success_message=f"User {username} added with privilege level {privilege}.")

    def modify_user(self, username: str, password: str = None, privilege: int = None):
        """
        Modifies an existing user with the specified username. Password and/or privilege level can be changed.

        Args:
            username (str): The username for the user.
            password (str): If provided, specifies a new password for the user. Min 4 to max 16 characters, case-sensitive.
            privilege (int): If provided, specifies a new privilege level for the user (1 to 4).
        
        Examples:
            >>> device.config.user.modify_user('testuser', password='newpassword')
            >>> device.config.user.modify_user('testuser', privilege=2)
        """
        command: str = Commands.CONFIG.USER.MODIFY(username, password, privilege)
        self._execute_config_command(command, success_message=f"User {username} modified.")

    def delete_user(self, username: str):
        """
        Deletes an existing user with the specified username.

        Args:
            username (str): The username for the user to delete.
        Examples:
            >>> device.config.user.delete_user('testuser')
        """
        command = Commands.CONFIG.USER.DELETE(username)
        self._execute_config_command(command, success_message=f"User {username} deleted.")

    def change_user_privilege(self, username: str, privilege: int):
        """
        Modifies the privilege level of an existing user.

        Args:
            username (str): The username of the user.
            privilege (int): The new privilege level for the user (1 to 4).
        Examples:
            >>> device.config.user.change_user_privilege('testuser', privilege=2)
        """
        self.modify_user(username, privilege=privilege)

    def deactivate_user(self, username: str):
        """
        Deactivates an existing user by setting their privilege to 'no login'.

        Args:
            username (str): The username of the user to deactivate.
            
        Examples:
            >>> device.config.user.deactivate_user('testuser')
        """
        self.change_user_privilege(username, privilege=4)