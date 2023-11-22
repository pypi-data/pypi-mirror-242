from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Response:
    host: str
    command: str
    exprct_string: str = None
    start_time: datetime = field(default_factory=datetime.now)
    finish_time: datetime = field(default_factory=datetime.now, init=False)
    elapsed_time: float = field(init=False)
    failed: bool = field(default=True, init=False)
    raw_output: str = field(default_factory=str, init=False)
    output: str = field(default_factory=str, init=False)
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__} <Command: {self.command}> <Expect: {self.exprct_string}> <Success: {not self.failed}> <Elapsed Time: {self.elapsed_time} sec>"
    
    def record_response(self, output: str, raw_output: str, failed: bool):
        self.finish_time = datetime.now()
        self.elapsed_time = (self.finish_time - self.start_time).total_seconds()
        self.failed = False
        self.output = output
        self.raw_output = raw_output
        self.failed = failed
        