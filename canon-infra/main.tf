provider "azurerm" {
  features {}

  subscription_id = "e5413124-3031-4576-b40a-19694c924851"
}

resource "azurerm_resource_group" "canon_rg" {
  name     = "canon-rg"
  location = var.location
}

resource "azurerm_postgresql_flexible_server" "canon_db" {
  name                   = "canon-postgres-server"
  resource_group_name    = azurerm_resource_group.canon_rg.name
  location               = var.location
  administrator_login    = var.postgres_admin
  administrator_password = var.postgres_password
  version                = "14"
  sku_name               = "B_Standard_B1ms"
  storage_mb             = 32768
  zone                   = "1"
  public_network_access_enabled = true
}

data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "canon_kv" {
  name                        = "canonkeyvault5678"
  location                    = azurerm_resource_group.canon_rg.location
  resource_group_name         = azurerm_resource_group.canon_rg.name
  tenant_id                   = "a4703bc0-dd58-4f0e-b452-1580f75265d1"
  sku_name                    = "standard"
  soft_delete_retention_days  = 90
  public_network_access_enabled = true

  access_policy {
    tenant_id = "a4703bc0-dd58-4f0e-b452-1580f75265d1"
    object_id = "049138e7-8772-46b2-ae32-55d52927918a"

    secret_permissions = [
      "Get",
      "List",
      "Set"
    ]
  }
}

resource "azurerm_key_vault_secret" "db_password" {
  name         = "PostgresPassword"
  value        = var.postgres_password
  key_vault_id = azurerm_key_vault.canon_kv.id
}