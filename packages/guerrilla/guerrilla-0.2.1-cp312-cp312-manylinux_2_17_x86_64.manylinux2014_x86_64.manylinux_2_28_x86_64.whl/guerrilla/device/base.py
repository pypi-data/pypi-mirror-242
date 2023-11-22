from dataclasses import dataclass, field
from guerrilla.connection import Session
from guerrilla.connection.session import BaseSession
from guerrilla.logging import logger
from guerrilla.connection.response import Response
from typing import Union, List, Optional, Callable

@dataclass
class BaseDevice:
    config: dict
    session: BaseSession = field(init=False)
    logger = logger

    def __post_init__(self):
        self.name = self.config.get("name", None)
        self.session = Session(config=self.config)

    def connect(self) -> None:
        self.session.connect()

    def disconnect(self) -> None:
        self.session.disconnect()

    def run(self, 
            command: str, 
            expect_string: str = None, 
            read_timeout: int = 30, 
            error_detector: Optional[Callable[[str], bool]] = None, 
            extend_error: Union[str, List[str], None] = None
            ) -> Response:
        response = Response(self.name, command, expect_string)
        output, raw_output, failed = self.session.run(command, 
                                                        expect_string=expect_string, 
                                                        read_timeout=read_timeout,
                                                        error_detector=error_detector,
                                                        extend_error=extend_error
                                                        )
        response.record_response(output, raw_output, failed)
        return response

    def run_timing(self, command: str, last_read: int = 2) -> str:
        return self.session.run_timing(command, last_read)

    def find_prompt(self) -> str:
        return self.session.find_prompt()

    @property
    def status(self) -> str:
        return self.session.status


@dataclass
class Device:
    config: dict

    def __new__(cls, config: dict):
        device_model = config.get("type", None)
        if device_model == "router":
            from .router import Router
            return Router(config)
        elif device_model == "linux":
            from .linux import Linux
            return Linux(config)
        else:
            raise NotImplementedError(f"Device type {device_model} not implemented")

