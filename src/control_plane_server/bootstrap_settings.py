import os
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class BootstrapSettings():
    environment: str
    super_user_login: str
    super_user_password: str
    
def load_bootstrap_settings() -> BootstrapSettings:
    return BootstrapSettings(
        environment=os.environ["ENVIRONMENT"],
        super_user_login=os.environ["SUPER_USER_LOGIN"],
        super_user_password=os.environ["SUPER_USER_PASSWORD"]
    )