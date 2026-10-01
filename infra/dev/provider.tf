terraform {
  required_providers {
    postgresql = {
      source  = "cyrilgdn/postgresql"
      version = "1.27.0"
    }
  }
}

provider "postgresql" {
  host            = var.POSTGRES_HOST
  port            = var.POSTGRES_PORT
  database        = "postgres"
  username        = var.POSTGRES_USER
  password        = var.POSTGRES_PASSWORD
  sslmode         = "disable"
  connect_timeout = 15
}
