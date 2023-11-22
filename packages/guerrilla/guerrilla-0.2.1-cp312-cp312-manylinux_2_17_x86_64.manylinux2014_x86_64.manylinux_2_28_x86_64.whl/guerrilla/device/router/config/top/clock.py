from typing import SupportsIndex, Union
from guerrilla.device.router.config import BaseConfig
from guerrilla.device.router.command import Commands
class Clock(BaseConfig):
    
    extend_error: list[str] = [
            'Minute must be in the range from 0 to 59.',
            'Hour must be in the range from 0 to 23.'
            ] # BUG: The router cli will raise error.
    
    def set_clock(self, year: SupportsIndex, month: SupportsIndex, day: SupportsIndex, hh: SupportsIndex, mm: SupportsIndex, ss: SupportsIndex):
        """
        Sets the clock of the router device to the specified date and time.

        Args:
            year (int): The year.
            month (int): The month.
            day (int): The day.
            hh (int): The hour.
            mm (int): The minute.
            ss (int): The second.
            
        Example:
            >>> device.config.clock.set_clock(year=2023, month=11, day=14, hh=20, mm=57, ss=30)
        """
        cmd: str = Commands.CONFIG.CLOCK.SET(hh, mm, ss, month, day, year)
        self._execute_config_command(cmd, success_message=f"Clock set to {hh}:{mm}:{ss} {month} {day} {year}")
        
    def set_timezone(self,offset_hour: int):
        """
        Sets the timezone of the router device to the specified offset hour.

        Args:
            offset_hour (int): The offset hour.
        
        Example:
            >>> device.config.clock.set_timezone(offset_hour=8)
        """
        cmd: str = Commands.CONFIG.CLOCK.TIMEZONE(offset_hour)
        self._execute_config_command(cmd, success_message=f"Timezone set to {offset_hour}")
            
    def set_summer_time_start(self, month: Union[str, int], week:Union[str, int], day:Union[str, int], hh: SupportsIndex, mm: SupportsIndex):
        """
        Sets the start of the summer time based on the month provided.
        The month can be a string like 'Jan', 'January', or an integer 1-12.
        
        Examples:
            >>> device.config.clock.set_summer_time_start(month=3, week=2, day=1, hh=2, mm=0)
            >>> device.config.clock.set_summer_time_start('Mar', '1st', 'Sun', 22, 35)
        """
        
        cmd: str = Commands.CONFIG.CLOCK.SUMMER_START_TIME(month, week, day, hh, mm)
        self._execute_config_command(cmd, success_message=f"Summer time start set to {month} {week} {day} {hh} {mm}", extend_error=self.extend_error)
            
    def set_summer_time_end(self, month: Union[str, int], week:Union[str, int], day:Union[str, int], hh: SupportsIndex, mm: SupportsIndex):
        """
        Sets the end of the summer time based on the month provided.
        The month can be a string like 'Jan', 'January', or an integer 1-12.
        
        Examples:
            >>> device.config.clock.set_summer_time_end(month=3, week=2, day=1, hh=2, mm=0)
            >>> device.config.clock.set_summer_time_end('Mar', '1st', 'Sun', 22, 35)
        """
        cmd:str = Commands.CONFIG.CLOCK.SUMMER_END_TIME(month, week, day, hh, mm)
        self._execute_config_command(cmd, success_message=f"Summer time end set to {month} {week} {day} {hh} {mm}", extend_error=self.extend_error)

    def set_summer_time_offset(self, offset_hour: int):
        """
        Sets the summer time offset hour.
        
        Examples:
            >>> device.config.clock.set_summer_time_offset(offset_hour=1)
        """
        cmd: str = Commands.CONFIG.CLOCK.SUMMER_TIME_OFFSET(offset_hour)
        self._execute_config_command(cmd, success_message=f"Summer time offset set to {offset_hour}")
