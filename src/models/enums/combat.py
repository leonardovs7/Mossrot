from enum import Enum, auto

class StatusEffect(Enum):
    NONE = auto()
    # Debuffs (Negativos)
    BLEEDING = auto()  # Dano físico por turno (Cortes)
    POISONED = auto()  # Dano químico + redução de ataque
    INFECTED = auto()  # Efeito do Mofo: Dano que escala com o tempo
    STUNNED = auto()  # Perda de turno

    # Buffs (Positivos)
    FOCUSED = auto()  # Aumento de crítico/precisão (Efeito do Âmbar)
    REGEN = auto()  # Recuperação passiva de HP