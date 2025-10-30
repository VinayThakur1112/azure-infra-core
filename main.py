#!/usr/bin/env python3
"""
main.py - Unified CLI / Interactive entry point for:
  - Resource Service (create/delete resource groups)
  - Data Pipeline (placeholder)
  - Model Deployment (placeholder)

Behavior is controlled by config/config.json (interactive true/false).
"""

import sys
import time
import json
import os
from colorama import Fore, Style, init

# Import resource functions (assumes azure_resource_group.py exists in same folder)
from src.resource_group import create_resource_group, delete_resource_group
from src.virtual_environment import create_vm

# Initialize colorama
init(autoreset=True)



# -----------------------
# Config loader
# -----------------------
def load_app_config(config_file):
    config_path = os.path.join(os.path.dirname(__file__), "cfg", config_file)
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with open(config_path, "r") as f:
        return json.load(f)



# -----------------------
# UI / Printing helpers
# -----------------------
def print_divider(char="─"):
    print(f"{Fore.CYAN}{char * 60}{Style.RESET_ALL}")



def print_header_for():
    # Dynamic header depending on selected service
    print()
    print_divider("═")
    print(f"{Fore.CYAN}{Style.BRIGHT}⚙️  ⚙️  ⚙️  ⚙️  ⚙️  ⚙️  ⚙️  ⚙️  ⚙️  ⚙️  ⚙️  ⚙️  ")
    print_divider("═")
    print()



def print_usage():
    print(f"{Fore.YELLOW}Usage (non-interactive):{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python main.py resource create <env> <rg_name> \
          [location]{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python main.py resource delete <env> <rg_name>\
          {Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python main.py pipeline run <env> <pipeline_name>\
          {Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python main.py model deploy <env> <model_name>\
          {Style.RESET_ALL}")
    print()
    print(f"{Fore.LIGHTBLACK_EX}Run without args when interactive mode is \
          ON in config.{Style.RESET_ALL}\n")



def status(msg, kind="info"):
    icons = {
        "info": f"{Fore.CYAN}ℹ️ ",
        "action": f"{Fore.MAGENTA}🚀 ",
        "success": f"{Fore.GREEN}✅ ",
        "warn": f"{Fore.YELLOW}⚠️ ",
        "error": f"{Fore.RED}❌ ",
    }
    print(f"{icons.get(kind, '')}{msg}{Style.RESET_ALL}")



# -----------------------
# Interactive flows
# -----------------------
def interactive_menu():
    print()
    status("Interactive mode enabled.", "info")
    # choose service
    print("Select project:")
    print(f"  1) my-mlops")
    print(f"  2) my-llm")
    print(f"  3) guest-sense-app")
    choice = input(f"\nEnter choice [1-3] (default 1): ").strip() or "1"

    if choice not in ("1", "2", "3", "4"):
        status("Invalid choice. Exiting.", "error")
        return

    if choice == "1":
        interactive_mymlops_project()



def interactive_creation(cfg):
    print_header_for()

    print("\nSelect service:")
    print("  1) Resource group creation")
    print("  2) Resource group deleteion")
    print("  3) Virtual Machine creation")
    print("  4) Virtual Machine deletion")
    print("  98) Delete costly service")
    print("  99) Delete all")
    a = input("Enter choice [1-2] (default 1): ").strip() or "1"

    if a == "1":
        # Fetch resource group and location directly from config
        # rg_name = input(f"Resource group name [{rg_name or 'none'}]: ").strip() 
        rg_config = cfg.get("resource_group", {})
        subscription_id = cfg.get("subscription_id", {})
        rg_name = rg_config.get("name")
        location = rg_config.get("location", "eastus")
        print(f"rg_name: {rg_name}")
        print(f"location: {location}")
        
        status(f"🚀 Creating resource group '{rg_name}' in '{location}'...", "action")
        create_resource_group(rg_name, location, subscription_id)
        status("✅ Create operation completed successfully.", "success")

    if a == "2":
        # Fetch resource group and location directly from config
        # rg_name = input(f"Resource group name [{rg_name or 'none'}]: ").strip() 
        rg_config = cfg.get("resource_group", {})
        subscription_id = cfg.get("subscription_id", {})
        rg_name = rg_config.get("name")
        location = rg_config.get("location", "eastus")
        print(f"rg_name: {rg_name}")
        print(f"location: {location}")
        
        status(f"🚀 Deleting resource group '{rg_name}' in '{location}'...", "action")
        delete_resource_group(rg_name, subscription_id)
        status("✅ Delete operation completed successfully.", "success")

    if a == "3":
        # Fetch resource group and location directly from config
        # rg_name = input(f"Resource group name [{rg_name or 'none'}]: ").strip() 
        rg_config = cfg.get("resource_group", {})
        subscription_id = cfg.get("subscription_id", {})
        rg_name = rg_config.get("name")
        location = rg_config.get("location", "eastus")
        print(f"rg_name: {rg_name}")
        print(f"location: {location}")
        
        status(f"🚀 Deleting resource group '{rg_name}' in '{location}'...", "action")
        delete_resource_group(rg_name, subscription_id)
        status("✅ Delete operation completed successfully.", "success")



def interactive_mymlops_project():
    # TODO comment dev file for production
    # cfg = load_app_config("config_mymlops.json")
    cfg = load_app_config("config_mymlops_dev.json")

    print_header_for()

    print("\nSelect action:")
    print("  1) Interactive")
    print("  2) Create all service")
    print("  2) Delete costly service")
    print("  2) Delete all")
    a = input("Enter choice [1-2] (default 1): ").strip() or "1"

    if a == "1":
        interactive_creation(cfg)
    


# -----------------------
# Entry point
# -----------------------
def main():

    # If interactive mode enabled and no CLI args, run interactive menu
    interactive_menu()

if __name__ == "__main__":
    main()