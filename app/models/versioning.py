from dataclasses import dataclass


@dataclass
class StrategyVersion:
    edge_id: str
    version: str
    locked: bool
    trades_completed: int
