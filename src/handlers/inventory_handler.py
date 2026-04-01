from typing import Optional
from src.models.entities.item import Item

class InventoryHandler:
    @staticmethod
    def add_item(entity, item: Item) -> None:
        # Garante que o atributo existe para evitar quebra de código
        if hasattr(entity, 'inventory'):
            entity.inventory.append(item)
            print(f"[+] {entity.name} recolheu: {item.name}")

    @staticmethod
    def remove_item(entity, item: Item) -> bool:
        if hasattr(entity, 'inventory') and item in entity.inventory:
            entity.inventory.remove(item)
            return True
        return False

    @staticmethod
    def has_item_by_id(entity, target_id: str) -> bool:
        inventory = getattr(entity, 'inventory', [])
        return any(item.id == target_id for item in inventory)

    @staticmethod
    def get_item_by_id(entity, target_id: str) -> Optional[Item]:
        inventory = getattr(entity, 'inventory', [])
        return next((item for item in inventory if item.id == target_id), None)