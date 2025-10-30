import os
import json
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute.models import (
    HardwareProfile, OSProfile, LinuxConfiguration,
    SshConfiguration, SshPublicKey, NetworkInterfaceReference,
    StorageProfile, ImageReference, OSDisk, DiskCreateOptionTypes
)
from azure.mgmt.network.models import (
    NetworkSecurityGroup, SecurityRule, PublicIPAddress,
    NetworkInterface, Subnet, VirtualNetwork, IPConfiguration
)


# ---------------------------------------------------------------------
# Function 1: CREATE VIRTUAL MACHINE
# ---------------------------------------------------------------------
def create_vm(config_path="config/dev.json"):
    cfg = load_config(config_path)

    subscription_id = cfg["azure"]["subscription_id"]
    resource_group = cfg["resource_group"]["name"]
    location = cfg["resource_group"]["location"]
    vm_name = cfg["vm"]["name"]
    vm_size = cfg["vm"]["size"]
    admin_username = cfg["vm"]["admin_username"]
    ssh_key_path = os.path.expanduser(cfg["vm"]["ssh_public_key_path"])

    print(f"🚀 Starting VM creation: {vm_name} in {location}")

    credential = DefaultAzureCredential()
    resource_client = ResourceManagementClient(credential, subscription_id)
    network_client = NetworkManagementClient(credential, subscription_id)
    compute_client = ComputeManagementClient(credential, subscription_id)

    # Ensure resource group
    print(f"🔹 Ensuring resource group '{resource_group}' exists...")
    resource_client.resource_groups.create_or_update(resource_group, {"location": location})

    # Virtual Network
    print("🔹 Creating Virtual Network...")
    vnet = network_client.virtual_networks.begin_create_or_update(
        resource_group, "vnet-mlops",
        {"location": location, "address_space": {"address_prefixes": ["10.0.0.0/16"]}},
    ).result()

    # Subnet
    print("🔹 Creating Subnet...")
    subnet = network_client.subnets.begin_create_or_update(
        resource_group, "vnet-mlops", "subnet-mlops", {"address_prefix": "10.0.0.0/24"},
    ).result()

    # NSG (SSH only)
    print("🔹 Creating NSG (allow SSH)...")
    nsg = network_client.network_security_groups.begin_create_or_update(
        resource_group, "nsg-mlops",
        {
            "location": location,
            "security_rules": [
                SecurityRule(
                    name="AllowSSH", protocol="Tcp", direction="Inbound", access="Allow",
                    priority=1000, source_address_prefix="*", destination_address_prefix="*",
                    source_port_range="*", destination_port_range="22",
                )
            ],
        },
    ).result()

    # Public IP
    print("🔹 Creating Public IP...")
    public_ip = network_client.public_ip_addresses.begin_create_or_update(
        resource_group, "pip-mlops", {"location": location, "public_ip_allocation_method": \
                                      "Dynamic"},
    ).result()

    # Network Interface
    print("🔹 Creating Network Interface...")
    nic = network_client.network_interfaces.begin_create_or_update(
        resource_group, "nic-mlops",
        {
            "location": location,
            "ip_configurations": [
                IPConfiguration(
                    name="ipconfig1",
                    subnet=Subnet(id=subnet.id),
                    public_ip_address=PublicIPAddress(id=public_ip.id),
                    network_security_group=NetworkSecurityGroup(id=nsg.id),
                )
            ],
        },
    ).result()

    # VM Configuration
    print("🔹 Defining VM configuration...")
    with open(ssh_key_path, "r") as f:
        ssh_key_data = f.read().strip()

    vm_parameters = {
        "location": location,
        "hardware_profile": HardwareProfile(vm_size=vm_size),
        "storage_profile": StorageProfile(
            image_reference=ImageReference(
                publisher="Canonical",
                offer="0001-com-ubuntu-server-noble",
                sku="24_04-lts-gen2",
                version="latest",
            ),
            os_disk=OSDisk(
                create_option=DiskCreateOptionTypes.from_image,
                managed_disk={"storage_account_type": "StandardSSD_LRS"},
            ),
        ),
        "os_profile": OSProfile(
            computer_name=vm_name,
            admin_username=admin_username,
            linux_configuration=LinuxConfiguration(
                disable_password_authentication=True,
                ssh=SshConfiguration(
                    public_keys=[
                        SshPublicKey(
                            path=f"/home/{admin_username}/.ssh/authorized_keys",
                            key_data=ssh_key_data,
                        )
                    ]
                ),
            ),
        ),
        "network_profile": {"network_interfaces": [NetworkInterfaceReference(id=nic.id)]},
    }

    # Create the VM
    print(f"🚀 Creating VM '{vm_name}' ... this may take a few minutes.")
    creation = compute_client.virtual_machines.begin_create_or_update(
        resource_group, vm_name, vm_parameters
    )
    creation.result()

    print(f"✅ VM '{vm_name}' created successfully in {location}.")


# ---------------------------------------------------------------------
# Function 2: STOP VM (graceful shutdown)
# ---------------------------------------------------------------------
def stop_vm(config_path="config/dev.json"):
    cfg = load_config(config_path)
    subscription_id = cfg["azure"]["subscription_id"]
    resource_group = cfg["resource_group"]["name"]
    vm_name = cfg["vm"]["name"]

    credential = DefaultAzureCredential()
    compute_client = ComputeManagementClient(credential, subscription_id)

    print(f"🛑 Stopping VM '{vm_name}'...")
    async_stop = compute_client.virtual_machines.begin_power_off(resource_group, vm_name)
    async_stop.result()
    print(f"✅ VM '{vm_name}' stopped successfully.")


# ---------------------------------------------------------------------
# Function 3: DEALLOCATE VM (stop billing)
# ---------------------------------------------------------------------
def deallocate_vm(config_path="config/dev.json"):
    cfg = load_config(config_path)
    subscription_id = cfg["azure"]["subscription_id"]
    resource_group = cfg["resource_group"]["name"]
    vm_name = cfg["vm"]["name"]

    credential = DefaultAzureCredential()
    compute_client = ComputeManagementClient(credential, subscription_id)

    print(f"💤 Deallocating VM '{vm_name}' (releases compute)...")
    async_deallocate = compute_client.virtual_machines.begin_deallocate(
        resource_group, vm_name)
    
    async_deallocate.result()
    print(f"✅ VM '{vm_name}' deallocated successfully (no compute cost).")


# ---------------------------------------------------------------------
# Main execution block (for quick test)
# ---------------------------------------------------------------------
if __name__ == "__main__":
    # Example usage:
    # create_vm()
    # stop_vm()
    # deallocate_vm()
    create_vm()