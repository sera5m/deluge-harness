"""Minimal node registry placeholder for Deluge Harness.

Head maintains the live registry. Workers heartbeat to update availability.
"""
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import json

@dataclass
class Node:
    name: str
    hostname: str
    role: str  # head | worker | specialist
    availability: str = "offline"  # online | paused | offline
    listed_availability: str = ""
    is_bulk_storage: bool = False
    models: List[str] = field(default_factory=list)
    organs: List[str] = field(default_factory=list)
    gpu: str = ""
    cpu: str = ""
    ram_gb: float = 0.0
    endpoint: str = ""
    last_heartbeat: Optional[str] = None
    notes: str = ""

    def to_dict(self):
        return self.__dict__

class NodeRegistry:
    def __init__(self):
        self.nodes: dict[str, Node] = {}

    def register(self, node: Node):
        self.nodes[node.name] = node

    def update_heartbeat(self, name: str, availability: str, endpoint: Optional[str] = None):
        if name in self.nodes:
            n = self.nodes[name]
            n.availability = availability
            n.last_heartbeat = datetime.utcnow().isoformat()
            if endpoint:
                n.endpoint = endpoint

    def available_workers(self, capability: Optional[str] = None) -> List[Node]:
        result = []
        for n in self.nodes.values():
            if n.availability != "online" or n.role == "head":
                continue
            if capability and capability not in n.models and capability not in n.organs:
                continue
            result.append(n)
        return result

    def get(self, name: str) -> Optional[Node]:
        return self.nodes.get(name)

    def dump(self) -> str:
        return json.dumps({k: v.to_dict() for k, v in self.nodes.items()}, indent=2)
