# Reference the existing Resource Group we already created in Phase 1
data "azurerm_resource_group" "rg" {
  name = var.resource_group_name
}

# Reference the existing Azure Container Registry we created in Phase 1
data "azurerm_container_registry" "acr" {
  name                = "auroraaudioacrprod"
  resource_group_name = data.azurerm_resource_group.rg.name
}

# Build the AKS Cluster
resource "azurerm_kubernetes_cluster" "aks" {
  name                = var.cluster_name
  location            = var.location
  resource_group_name = data.azurerm_resource_group.rg.name
  dns_prefix          = var.cluster_name

  default_node_pool {
    name       = "nodepool"
    node_count = 1
    vm_size    = "Standard_DS2_v2" # Standard enterprise burstable size
  }

  identity {
    type = "SystemAssigned"
  }
}

# Grant the AKS cluster permission to securely pull images from the ACR
resource "azurerm_role_assignment" "aks_to_acr" {
  principal_id                     = azurerm_kubernetes_cluster.aks.kubelet_identity[0].object_id
  role_definition_name             = "AcrPull"
  scope                            = data.azurerm_container_registry.acr.id
  skip_service_principal_aad_check = true
}

output "kube_config" {
  value     = azurerm_kubernetes_cluster.aks.kube_config_raw
  sensitive = true
}
