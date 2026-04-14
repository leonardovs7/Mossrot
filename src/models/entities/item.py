from dataclasses import dataclass
from src.models.enums import ItemCategory, ItemSubcategory, StatusEffect


#from typing import Optional, Callable

@dataclass
class Item:
    id: str
    name: str #nome do item
    description: str #descricao do item
    category: ItemCategory #categoria do item
    subcategory: ItemSubcategory #subcategoria do item
    status_effect: StatusEffect #status que o item aplica
    is_consumable: bool #o item é consumivel
    is_equippable: bool #o item é equipavel
    is_equipped: bool #o item esta equipado
    value: int #valor de atributo do item
    passive_bonus: int #valor de atributo de status passivo
    stackable: bool #se o item é estacavel
    quantity: int #qtd de itens iguais no inv

@dataclass
class LightEquipment(Item):
    fuel: float #combustivel
    max_fuel: float #combustivel maximo
    fuel_consume: float #taxa de consumo
    is_lit: bool #esta acesso

    def __str__(self):
        return f"{self.name}: {self.description}"
