import argparse
from dataclasses import dataclass
from typing import Literal
from collections.abc import Sequence

@dataclass(frozen=True, slots=True)
class BootstrapSettings():
    environment: Literal["DEV", "PROD"]
    def __post_init__(self) -> None:
        if self.environment not in ("PROD", "DEV"):
            raise ValueError("environment должен быть PROD или DEV")
        
    super_user_login: str
    super_user_password: str
    
def parse_cli_args(cli_args: Sequence[str] | None = None) -> BootstrapSettings:
    