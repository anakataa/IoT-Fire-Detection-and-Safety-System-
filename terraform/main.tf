terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# -------------------------
# 1. Resource Group
# -------------------------
resource "azurerm_resource_group" "rg" {
  name     = "${var.prefix}-rg"
  location = var.location
}

# -------------------------
# 2. Virtual Network (VNet)
# -------------------------
resource "azurerm_virtual_network" "vnet" {
  name                = "${var.prefix}-vnet"
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name
  address_space       = ["10.0.0.0/16"]
}

# -------------------------
# 3. Subnet for VM
# -------------------------
resource "azurerm_subnet" "subnet" {
  name                 = "${var.prefix}-subnet"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.1.0/24"]
}

# -------------------------
# 4. Network Security Group (NSG)
# -------------------------
resource "azurerm_network_security_group" "nsg" {
  name                = "${var.prefix}-nsg"
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_network_security_rule" "allow_mqtt" {
  name                        = "allow_mqtt"
  priority                    = 100
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "1883"
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  network_security_group_name = azurerm_network_security_group.nsg.name
  resource_group_name         = azurerm_resource_group.rg.name
}

resource "azurerm_network_security_rule" "allow_http" {
  name                        = "allow_http"
  priority                    = 101
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "8080"
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  network_security_group_name = azurerm_network_security_group.nsg.name
  resource_group_name         = azurerm_resource_group.rg.name
}

# -------------------------
# Public IP for MQTT Broker VM
# -------------------------
resource "azurerm_public_ip" "mqtt_broker_public_ip" {
  name                = "${var.prefix}-mqtt-broker-ip"
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name
  allocation_method   = "Static"
}

# -------------------------
# Network Interface for MQTT Broker VM
# -------------------------
resource "azurerm_network_interface" "mqtt_broker_nic" {
  name                = "${var.prefix}-mqtt-broker-nic"
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.subnet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.mqtt_broker_public_ip.id
  }
}

# -------------------------
# Network Interface Association with NSG
# -------------------------
resource "azurerm_network_interface_security_group_association" "mqtt_broker_nsg" {
  network_interface_id      = azurerm_network_interface.mqtt_broker_nic.id
  network_security_group_id = azurerm_network_security_group.nsg.id
}

# -------------------------
# 5. MQTT Broker VM
# -------------------------
resource "azurerm_virtual_machine" "mqtt_broker" {
  name                = "${var.prefix}-mqtt-broker"
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name
  network_interface_ids = [
    azurerm_network_interface.mqtt_broker_nic.id
  ]
  vm_size             = "Standard_B1s"
  storage_os_disk {
    name              = "${var.prefix}-mqtt-broker-osdisk"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Standard_LRS"
  }
  os_profile {
    computer_name  = "mqtt-broker"
    admin_username = "azureuser"
    admin_password = var.admin_password
  }
  os_profile_linux_config {
    disable_password_authentication = false
  }
}

# -------------------------
# Public IP for Backend API VM
# -------------------------
resource "azurerm_public_ip" "backend_api_public_ip" {
  name                = "${var.prefix}-backend-api-ip"
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name
  allocation_method   = "Static"
}

# -------------------------
# Network Interface for Backend API VM
# -------------------------
resource "azurerm_network_interface" "backend_api_nic" {
  name                = "${var.prefix}-backend-api-nic"
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.subnet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.backend_api_public_ip.id
  }
}

# -------------------------
# Network Interface Association with NSG
# -------------------------
resource "azurerm_network_interface_security_group_association" "backend_api_nsg" {
  network_interface_id      = azurerm_network_interface.backend_api_nic.id
  network_security_group_id = azurerm_network_security_group.nsg.id
}

# -------------------------
# 6. Backend API VM
# -------------------------
resource "azurerm_virtual_machine" "backend_api" {
  name                = "${var.prefix}-backend-api"
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name
  network_interface_ids = [
    azurerm_network_interface.backend_api_nic.id
  ]
  vm_size             = "Standard_B1s"
  storage_os_disk {
    name              = "${var.prefix}-backend-api-osdisk"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Standard_LRS"
  }
  os_profile {
    computer_name  = "backend-api"
    admin_username = "azureuser"
    admin_password = var.admin_password
  }
  os_profile_linux_config {
    disable_password_authentication = false
  }
}

# -------------------------
# Public IP for PostgreSQL VM
# -------------------------
resource "azurerm_public_ip" "postgres_public_ip" {
  name                = "${var.prefix}-postgres-ip"
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name
  allocation_method   = "Static"
}

# -------------------------
# Network Interface for PostgreSQL VM
# -------------------------
resource "azurerm_network_interface" "postgres_nic" {
  name                = "${var.prefix}-postgres-nic"
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.subnet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.postgres_public_ip.id
  }
}

# -------------------------
# Network Interface Association with NSG
# -------------------------
resource "azurerm_network_interface_security_group_association" "postgres_nsg" {
  network_interface_id      = azurerm_network_interface.postgres_nic.id
  network_security_group_id = azurerm_network_security_group.nsg.id
}

# -------------------------
# 7. PostgreSQL VM
# -------------------------
resource "azurerm_virtual_machine" "postgres_vm" {
  name                = "${var.prefix}-postgres-vm"
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name
  network_interface_ids = [
    azurerm_network_interface.postgres_nic.id
  ]
  vm_size             = "Standard_B1s"
  storage_os_disk {
    name              = "${var.prefix}-postgres-osdisk"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Standard_LRS"
  }
  os_profile {
    computer_name  = "postgres-vm"
    admin_username = "azureuser"
    admin_password = var.admin_password
  }
  os_profile_linux_config {
    disable_password_authentication = false
  }
}