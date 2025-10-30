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
from infra.resource_group import create_resource_group, delete_resource_group

# Initialize colorama
init(autoreset=True)


# -----------------------
# Config loader
# -----------------------
def load_app_config():
    # TODO change the config file to config.json
    config_path = os.path.join(os.path.dirname(__file__), "config", "config_dev.json")
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with open(config_path, "r") as f:
        return json.load(f)


# -----------------------
# UI / Printing helpers
# -----------------------
def print_divider(char="─"):
    print(f"{Fore.CYAN}{char * 60}{Style.RESET_ALL}")


def print_header_for(service_name):
    # Dynamic header depending on selected service
    title_map = {
        "resource": "Resource Management Service",
        "pipeline": "Data Pipeline Service",
        "model": "Model Deployment Service"
    }
    subtitle = title_map.get(service_name, "Azure Tooling")
    print()
    print_divider("═")
    print(f"{Fore.CYAN}{Style.BRIGHT}⚙️  {subtitle.center(46)}")
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
# Placeholder functions for pipeline / model
# -----------------------
def run_pipeline(env_name, pipeline_name, cfg):
    """
    Placeholder: replace this with your actual pipeline invocation.
    """
    print_header_for("pipeline")
    status(f"Preparing to run pipeline '{pipeline_name}' in env '{env_name}'...", "action")
    # Example: access config values if needed
    contact = cfg.get("contact_email", "n/a")
    status(f"Contact: {contact}", "info")
    # Simulate long-running task
    time.sleep(1.0)
    status(f"Pipeline '{pipeline_name}' finished successfully.", "success")


def deploy_model(env_name, model_name, cfg):
    """
    Placeholder: replace this with your model deployment logic.
    """
    print_header_for("model")
    status(f"Preparing to deploy model '{model_name}' in env '{env_name}'...", "action")
    time.sleep(1.0)
    status(f"Model '{model_name}' deployed successfully.", "success")


# -----------------------
# Interactive flows
# -----------------------
def interactive_menu(cfg):
    print()
    status("Interactive mode enabled.", "info")
    # choose service
    print("Select service:")
    print(f"  1) Infra Service")
    print(f"  2) Pipeline Service")
    print(f"  3) Deployment Service")
    choice = input(f"\nEnter choice [1-3] (default 1): ").strip() or "1"

    if choice not in ("1", "2", "3"):
        status("Invalid choice. Exiting.", "error")
        return

    if choice == "1":
        interactive_resource_flow(cfg)
    elif choice == "2":
        interactive_pipeline_flow(cfg)
    else:
        interactive_model_flow(cfg)


def interactive_resource_flow(cfg):
    print_header_for("resource")
    env_name = input(f"Environment [{cfg.get('default_env', 'dev')}]: ").strip() \
        or cfg.get("default_env", "dev")
    status(f"Selected env: {env_name}", "info")

    print("\nSelect action:")
    print("  1) Create Resource Group")
    print("  2) Delete Resource Group")
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
        create_resource_group(env_name, rg_name, location, subscription_id)
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
        
        status(f"🚀 Creating resource group '{rg_name}' in '{location}'...", "action")
        delete_resource_group(env_name, rg_name, subscription_id)
        status("✅ Delete operation completed successfully.", "success")
    else:
        status("Invalid action selected.", "error")


def interactive_pipeline_flow(cfg):
    print_header_for("pipeline")
    env_name = input(f"Environment [{cfg.get('default_env', 'dev')}]: ").strip() \
        or cfg.get("default_env", "dev")
    pipeline_name = input("Pipeline name to run: ").strip()
    if not pipeline_name:
        status("Pipeline name is required. Aborting.", "error")
        return
    status(f"Running pipeline '{pipeline_name}' in env '{env_name}'...", "action")
    run_pipeline(env_name, pipeline_name, cfg)


def interactive_model_flow(cfg):
    print_header_for("model")
    env_name = input(f"Environment [{cfg.get('default_env', 'dev')}]: ").strip() \
        or cfg.get("default_env", "dev")
    
    model_name = input("Model name to deploy: ").strip()
    if not model_name:
        status("Model name is required. Aborting.", "error")
        return
    status(f"Deploying model '{model_name}' in env '{env_name}'...", "action")
    deploy_model(env_name, model_name, cfg)


# -----------------------
# Entry point
# -----------------------
def main():
    try:
        cfg = load_app_config()
        print(f"{Fore.LIGHTBLACK_EX} Configuration load done")

    except Exception as e:
        print(f"{Fore.RED}Failed to load config: {e}{Style.RESET_ALL}")
        sys.exit(1)

    is_interactive = bool(cfg.get("interactive", False))
    print(f"{Fore.LIGHTBLACK_EX} is_interactive: {is_interactive}")

    # If interactive mode enabled and no CLI args, run interactive menu
    if is_interactive and len(sys.argv) == 1:
        interactive_menu(cfg)
        return

    # Non-interactive: expect CLI args (service action ...)
    if len(sys.argv) == 1:
        # No args provided and interactive is off
        print_header_for("resource")
        status("No arguments provided and interactive mode is disabled.", "error")
        print_usage()
        return


if __name__ == "__main__":
    main()