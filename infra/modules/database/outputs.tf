output "database_name" {
  description = "Имя базы данных PostgreSQL."
  value       = postgresql_database.this.name
}
