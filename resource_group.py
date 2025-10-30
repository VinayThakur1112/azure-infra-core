import json
import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient


def get_resource_client(subscription_id):
    """Authenticate and return the ResourceManagementClient"""
    credential = DefaultAzureCredential()
    return ResourceManagementClient(credential, subscription_id)


def validate_resource_group(resource_client, rg_name):
    """Check if a resource group exists"""
    print(f"🔍 Validating resource group '{rg_name}'...")
    exists = resource_client.resource_groups.check_existence(rg_name)
    if exists:
        print(f"✅ Resource group '{rg_name}' exists.")
    else:
        print(f"❌ Resource group '{rg_name}' does not exist.")
    return exists


def create_resource_group(env_name, rg_name, location, subscription_id):
    """Create a resource group after validating"""
    print("create_resource_group function called")

    resource_client = get_resource_client(subscription_id)

    if validate_resource_group(resource_client, rg_name):
        print(f"ℹ️ Resource group '{rg_name}' already exists. Skipping creation.")
        return

    print(f"🚀 Creating resource group '{rg_name}' in '{location}'...")
    rg_result = resource_client.resource_groups.create_or_update(
        rg_name, {"location": location}
    )
    print(f"✅ Resource group '{rg_result.name}' created successfully.")


def delete_resource_group(env_name, rg_name, subscription_id):
    """Delete a resource group after validating"""

    resource_client = get_resource_client(subscription_id)

    if not validate_resource_group(resource_client, rg_name):
        print(f"⚠️ Resource group '{rg_name}' does not exist. Nothing to delete.")
        return

    print(f"🧹 Deleting resource group '{rg_name}'...")
    delete_poller = resource_client.resource_groups.begin_delete(rg_name)
    delete_poller.wait()
    print(f"✅ Resource group '{rg_name}' deleted successfully.")