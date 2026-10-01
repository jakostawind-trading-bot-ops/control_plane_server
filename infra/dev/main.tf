module "database" {
  source        = "../modules/database"
  database_name = "control_plane_dev"
}

moved {
  from = postgresql_database.control_plane
  to   = module.database.postgresql_database.this
}
