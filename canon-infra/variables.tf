variable "location" {
  default = "eastasia"
}

variable "postgres_admin" {
  default = "canonuser"
}

variable "postgres_password" {
  description = "Admin password for PostgreSQL"
  sensitive   = true
}
