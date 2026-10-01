variable "POSTGRES_USER" {
  type = string
}

variable "POSTGRES_PASSWORD" {
  type      = string
  sensitive = true
}

variable "POSTGRES_HOST" {
  type = string
}

variable "POSTGRES_PORT" {
  type = number
}
