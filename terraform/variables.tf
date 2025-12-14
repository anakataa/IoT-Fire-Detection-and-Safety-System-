variable "location" {
  description = "The Azure location for resources"
  default     = "eastus2"
}

variable "prefix" {
  description = "Prefix to use for naming resources"
  default     = "iot-fire-sys"
}

variable "admin_password" {
  description = "Admin password for PostgreSQL and VM"
  default     = "securepassword"
}

variable "db_username" {
  description = "Username for PostgreSQL database"
  default     = "iot_admin"
}