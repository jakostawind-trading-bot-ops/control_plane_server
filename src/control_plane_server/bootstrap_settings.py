import os
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class BootstrapSettings():
    environment: str
    super_user_login: str
    super_user_password: str
    
    #============================= DATABASE ==============================
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str
    
def load_bootstrap_settings() -> BootstrapSettings:
    return BootstrapSettings(
        environment=os.environ["ENVIRONMENT"],
        super_user_login=os.environ["SUPER_USER_LOGIN"],
        super_user_password=os.environ["SUPER_USER_PASSWORD"],
        
        db_host=os.environ["POSTGRES_HOST"],
        db_port=os.environ["POSTGRES_PORT"],
        db_name=os.environ["POSTGRES_DB"],
        db_user=os.environ["POSTGRES_USER"],
        db_password=os.environ["POSTGRES_PASSWORD"],
    )