
class GuerrillaSettingError(Exception):
    """Exception raised for errors in the setting file.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)