import os
from pathlib import Path
from typing import Any, Dict, Optional, List

import yaml

# Default config lives in the user's home directory. A bundled sample is used
# as a fallback when the file doesn't exist.
DEFAULT_CONFIG_FILE = Path.home() / ".chatops" / "config.yaml"
SAMPLE_CONFIG_FILE = Path(__file__).with_name("config.yaml")

# Lists of official regions per provider
AZURE_REGIONS: List[str] = [
    "eastus",
    "eastus2",
    "westus",
    "westus2",
    "westus3",
    "centralus",
    "southcentralus",
    "northcentralus",
    "brazilsouth",
    "brazilsoutheast",
    "canadacentral",
    "canadaeast",
    "eastasia",
    "southeastasia",
    "australiaeast",
    "australiasoutheast",
    "australiacentral",
    "australiacentral2",
    "japaneast",
    "japanwest",
    "koreacentral",
    "koreasouth",
    "francecentral",
    "francesouth",
    "germanywestcentral",
    "germanynorth",
    "norwayeast",
    "norwaywest",
    "switzerlandnorth",
    "switzerlandwest",
    "uksouth",
    "ukwest",
    "westeurope",
    "northeurope",
    "southafricanorth",
    "southafricawest",
    "polandcentral",
    "israelcentral",
    "qatarcentral",
    "spaincentral",
    "italynorth",
    "mexicocentral",
]

AWS_REGIONS: List[str] = [
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2",
    "af-south-1",
    "ap-east-1",
    "ap-south-1",
    "ap-south-2",
    "ap-southeast-1",
    "ap-southeast-2",
    "ap-southeast-3",
    "ap-southeast-4",
    "ap-northeast-1",
    "ap-northeast-2",
    "ap-northeast-3",
    "ca-central-1",
    "eu-central-1",
    "eu-central-2",
    "eu-west-1",
    "eu-west-2",
    "eu-west-3",
    "eu-north-1",
    "eu-south-1",
    "eu-south-2",
    "me-south-1",
    "me-central-1",
    "sa-east-1",
    "il-central-1",
    "us-gov-west-1",
    "us-gov-east-1",
]

GCP_REGIONS: List[str] = [
    "asia-east1",
    "asia-east2",
    "asia-northeast1",
    "asia-northeast2",
    "asia-northeast3",
    "asia-south1",
    "asia-south2",
    "asia-southeast1",
    "asia-southeast2",
    "australia-southeast1",
    "australia-southeast2",
    "europe-central2",
    "europe-north1",
    "europe-west1",
    "europe-west2",
    "europe-west3",
    "europe-west4",
    "europe-west6",
    "europe-west8",
    "europe-west9",
    "europe-southwest1",
    "me-central1",
    "me-west1",
    "northamerica-northeast1",
    "northamerica-northeast2",
    "southamerica-east1",
    "southamerica-west1",
    "us-central1",
    "us-east1",
    "us-east4",
    "us-west1",
    "us-west2",
    "us-west3",
    "us-west4",
]


def _prompt_missing_value(key: str) -> str:
    """Prompt user for a missing config value."""
    return input(f"Enter value for {key}: ")


def _merge_env(config: Dict[str, Any]) -> None:
    """Override config values with environment variables."""
    env_map = {
        "default_environment": "CHATOPS_DEFAULT_ENV",
        "default_cloud": "CHATOPS_DEFAULT_CLOUD",
        "credentials.mode": "CHATOPS_CRED_MODE",
    }
    for path, var in env_map.items():
        if var in os.environ:
            parts = path.split(".")
            target = config
            for p in parts[:-1]:
                target = target.setdefault(p, {})
            target[parts[-1]] = os.environ[var]


def _expand_regions(cloud: str, env_conf: Dict[str, Any]) -> List[str]:
    """Return expanded region list handling 'all' shorthand."""
    regions = env_conf.get("regions")
    if not regions:
        return []
    if isinstance(regions, str) and regions.lower() == "all":
        regions = ["all"]
    if isinstance(regions, list) and len(regions) == 1 and regions[0] == "all":
        if cloud == "azure":
            return AZURE_REGIONS
        if cloud == "aws":
            return AWS_REGIONS
        if cloud == "gcp":
            return GCP_REGIONS
    return regions


def load_config(
    path: Optional[Path] = None,
    overrides: Optional[Dict[str, Any]] = None,
    env: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """Load and validate configuration data."""
    if env is None:
        env = os.environ
    if path is None:
        path = DEFAULT_CONFIG_FILE
    if not path.exists():
        # Fall back to bundled sample so the CLI works out of the box
        path = SAMPLE_CONFIG_FILE
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {DEFAULT_CONFIG_FILE}")
    with path.open("r", encoding="utf-8") as f:
        data: Dict[str, Any] = yaml.safe_load(f) or {}

    _merge_env(data)
    if overrides:
        for k, v in overrides.items():
            parts = k.split(".")
            target = data
            for p in parts[:-1]:
                target = target.setdefault(p, {})
            target[parts[-1]] = v

    credentials = data.setdefault("credentials", {})
    mode = credentials.get("mode")
    if mode is None:
        mode = _prompt_missing_value("credentials.mode")
        credentials["mode"] = mode

    return data


def select_runtime(config: Dict[str, Any]) -> Dict[str, Any]:
    """Select provider and environment at runtime."""
    cloud = config.get("default_cloud") or _prompt_missing_value("default cloud")
    provider_conf = config.get(cloud)
    if provider_conf is None:
        raise ValueError(f"Cloud provider {cloud} not configured")

    env_name = config.get("default_environment")
    envs = provider_conf.get("environments", {})
    if env_name not in envs:
        print(f"Available environments for {cloud}: {', '.join(envs.keys())}")
        env_name = _prompt_missing_value("environment")
    env_conf = envs.get(env_name)
    if env_conf is None:
        raise ValueError(f"Environment {env_name} not found for {cloud}")

    regions = _expand_regions(cloud, env_conf)
    if regions:
        print(f"Regions: {', '.join(regions)}")
    if cloud == "aws" and env_conf.get("profile"):
        print(f"AWS profile: {env_conf['profile']}")
    if cloud == "azure" and env_conf.get("subscription_id"):
        print(f"Azure subscription: {env_conf['subscription_id']}")
    if cloud == "gcp" and env_conf.get("project_id"):
        print(f"GCP project: {env_conf['project_id']}")

    return {
        "cloud": cloud,
        "environment": env_name,
        "config": env_conf,
    }


if __name__ == "__main__":
    cfg = load_config()
    runtime = select_runtime(cfg)
    print(runtime)
