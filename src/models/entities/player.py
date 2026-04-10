from dataclasses import dataclass, field
from typing import List, Optional
from src.models.entities.entity import Entity
from src.models.entities.item import Item


@dataclass
class Player(Entity):
    # --- Status Básicos ---
    hp: int = 15
    max_hp: int = 15
    level: int = 1
    base_damage: int = 4
    damage_reduction: float = 0.0
    current_xp: int = 0

    # --- Equipamentos
    weapon: str = "Mãos Machucadas"
    armor: str = "Roupas Velhas"
    current_weapon_damage: int = 0
    current_weapon_bonus: int = 0
    current_armor_defense: int = 0
    current_armor_bonus: int = 0

    # --- Sanidade (Mecânica de Terror) ---
    sanity: int = 100
    max_sanity: int = 100

    # --- Esporos (Mecânica de Respiração) ---
    spore_debt: int = 0

    # --- Inventário e Equipamento ---
    inventory: List[Item] = field(default_factory=list)
    equipped_weapon: Optional[Item] = None
    equipped_armor: Optional[Item] = None
    has_light: bool = False

    # --- Propriedades Dinâmicas  ---
    in_combat: bool = False

    @property
    def next_level_xp(self) -> int:
        """Calcula o XP necessário baseado no nível atual."""
        return int(10 * (1.5 ** (self.level - 1)))

   #@property
    #def total_damage(self) -> int:
        """Soma o dano base com o valor da arma equipada."""
        # Se tiver arma, usa o .value dela. Se não, bônus é 0.
        bonus = self.equipped_weapon.value if self.equipped_weapon else 0
        return self.base_damage + bonus

    #@property
    #def total_reduction(self) -> float:
        """Soma a redução base com o bônus da armadura."""
        bonus = self.equipped_armor.value if self.equipped_armor else 0.0
        return self.damage_reduction + bonus