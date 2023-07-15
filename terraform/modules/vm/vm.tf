data "azurerm_image" "test" {
  name                = "myPackerImage"
  resource_group_name = "${var.resource_group}"
}

resource "azurerm_network_interface" "ha" {
  name                = "${var.application_type}-${var.resource_type}-ha"
  location            = "${var.location}"
  resource_group_name = "${var.resource_group}"

  ip_configuration {
    name                          = "internal"
    subnet_id                     = "${var.subnet_id}"
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = "${var.public_ip_address_id}"
  }
}

resource "azurerm_linux_virtual_machine" "vm" {
  name                = "${var.application_type}-${var.resource_type}-vm"
  location            = "${var.location}"
  resource_group_name = "${var.resource_group}"
  size                = "Standard_DS1_v2"
  admin_username      = "${var.admin_username}"
  admin_password      = "${var.admin_password}"
  disable_password_authentication = false
  network_interface_ids = [azurerm_network_interface.ha.id]
  admin_ssh_key {
    username   = "${var.admin_username}"
    public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCho0zWq+dWRcvNktD+cmVvbU/rNTkxYXbq3liFnSOc9haqnfrlHxweKTLAWOthCl/eQNMfR1SkN6uZmC3Djl1XcZkqFqxOvOgMOruZiwVIuxFO84PTDUgwSOD04gmj+o4GJ+E8uUFC3z/M6b0aTOlx0kG1KJm/hhvO/LWsmg2NJ0Jmuikc0gzJ595hXaxjMIBFK+PrjNhvpIYHQH9MZoOYuhE7sDXwgJhjZjoGeLLGuPuCtkbw7IFSfxv8d1UmN1ql3OrCXcWoyDzsOEt/NWBV1df7UfWwkA5dkpGAiSiL3eQu9uVOC5EzsJQro2DecHGy2H3lYMbgl+lnitLPDTLM49+5Y9sgXJcHBodK7Bq5x2i0WEl4VAN6DVagQIQis8up3cFyZM1erafmwqDgfG+x/ykfbdHq16QTBN9XMndBTxSXlSHK7bDXlqEQhOPvHy5pJMOZnQp2QZc1MiBHprX+Cv4rEL+nGskg91upzyYaKMBdnx9m5OOFuxePtV/N6yU= asus@LAPTOP-C32O7TUB"
  }
  os_disk {
    caching           = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }
  source_image_id = data.azurerm_image.test.id
  # source_image_reference {
  #   publisher = "Canonical"
  #   offer     = "UbuntuServer"
  #   sku       = "18.04-LTS"
  #   version   = "latest"
  # }
}
