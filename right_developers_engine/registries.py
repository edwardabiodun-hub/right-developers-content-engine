from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .config_loader import load_json_subset_yaml
from .errors import ConfigurationError


@dataclass(frozen=True)
class DomainRegistries:
    worldview: dict[str, Any]
    audiences: dict[str, Any]
    pillars: dict[str, Any]
    canonical_ip: dict[str, Any]
    minerals: dict[str, Any]
    franchises: dict[str, Any]

    def concept_ids(self) -> set[str]:
        return {item["id"] for item in self.canonical_ip["concepts"]}

    def mineral(self, mineral_id: str) -> dict[str, Any]:
        for item in self.minerals["minerals"]:
            if item["id"] == mineral_id:
                return item
        raise ConfigurationError(f"Unknown mineral: {mineral_id}")


def load_domain_registries(config_dir: Path) -> DomainRegistries:
    documents = {
        "worldview": "worldview.yaml",
        "audiences": "audiences.yaml",
        "pillars": "content-pillars.yaml",
        "canonical_ip": "canonical-ip.yaml",
        "minerals": "minerals.yaml",
        "franchises": "franchises.yaml",
    }
    values = {name: load_json_subset_yaml(config_dir / filename) for name, filename in documents.items()}
    required = {
        "worldview": "north_star",
        "audiences": "audiences",
        "pillars": "pillars",
        "canonical_ip": "concepts",
        "minerals": "minerals",
        "franchises": "franchises",
    }
    for document, key in required.items():
        if not isinstance(values[document].get(key), list | str):
            raise ConfigurationError(f"Missing required registry field: {document}.{key}")
    return DomainRegistries(**values)
