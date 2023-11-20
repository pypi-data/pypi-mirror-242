from dataclasses import dataclass


@dataclass
class Default:
    voice: str = ""
    speed: int = 200
    volume: float = 1.0
