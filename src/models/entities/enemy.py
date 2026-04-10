from dataclasses import dataclass
from src.models.entities.entity import Entity

@dataclass
class Enemy(Entity):
    xp_reward: int #recompensa de xp ao vencer o inimigo