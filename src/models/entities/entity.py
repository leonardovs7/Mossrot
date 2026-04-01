from abc import ABC, abstractmethod
from dataclasses import dataclass, field

@dataclass
class Entity(ABC):
    name: str #nome da entidade
    level: int #level da entidade
    hp: int #vida atual
    max_hp: int #vida máxima da entidade
    base_damage: int #dano base
    damage_reduction: int #redução em defesa
    is_defending: bool = field(init=False, default=False) #define se está em estado de defesa

    @property
    def is_alive(self) -> bool:
        return self.hp > 0