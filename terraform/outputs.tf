output "mqtt_broker_ip" {
  description = "Public IP of the MQTT Broker VM"
  value       = azurerm_public_ip.mqtt_broker_public_ip.ip_address
}

output "backend_api_ip" {
  description = "Public IP of the Backend API VM"
  value       = azurerm_public_ip.backend_api_public_ip.ip_address
}

output "postgres_ip" {
  description = "Public IP of the PostgreSQL VM"
  value       = azurerm_public_ip.postgres_public_ip.ip_address
}

