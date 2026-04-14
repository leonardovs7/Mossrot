from enum import Enum, auto

class ItemCategory(Enum):
    # Equipamentos
    WEAPON = auto()
    ARMOR = auto()
    LIGHT = auto()

    # Consumíveis
    HEAL = auto()  # Vida
    SANITY = auto()  # Sanidade
    FUEL = auto()  # Combustível para lamparina

    # Progresso e Utilidade
    KEY = auto()  # Chaves, Pés de Cabra, Pás (itens de progressão)
    VIEW = auto()  # Itens de visão especial (Âmbar)
    LORE = auto()  # Itens apenas para leitura/história
    TRASH = auto()  # Itens sem utilidade imediata

class ItemSubcategory(Enum):
    STANDARD = auto()  # Itens com apenas um valor/função simples
    HYBRID = auto()  # Itens "Dual": ex HP + Sanidade
    UNIQUE = auto()  # Itens com lógica customizada ou flags (Âmbar)