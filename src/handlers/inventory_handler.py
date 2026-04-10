from typing import Optional
from src.models.entities.item import Item

class InventoryHandler:
        @staticmethod
        def add_item(entity, new_item: Item) -> None:
            """Adiciona item ao inventário, somando quantidade se já existir e for empilhável."""
            if not hasattr(entity, 'inventory'):
                return

            # 1. Tenta encontrar um item idêntico já presente no inventário
            existing_item = next((i for i in entity.inventory if i.id == new_item.id), None)

            # 2. Se o item for empilhável e já existir no bolso
            if existing_item and getattr(new_item, 'stackable', True):
                # Soma a quantidade do novo item à quantidade do que já existe
                add_quantity = getattr(new_item, 'quantity', 1)
                existing_item.quantity += add_quantity
                print(
                    f"[+] {entity.name} adicionou {add_quantity}x ao monte de {existing_item.name} (Total: {existing_item.quantity})")
            else:
                # 3. Se não existir ou não for empilhável (ex: armas), adiciona como novo slot
                entity.inventory.append(new_item)
                print(f"[+] {entity.name} recolheu: {new_item.name}")

        @staticmethod
        def remove_item(entity, item: Item, amount: int = 1) -> bool:
            """Remove uma quantidade do item. Se chegar a 0, remove o objeto da lista."""
            if not hasattr(entity, 'inventory') or item not in entity.inventory:
                return False

            # Se tiver mais do que a quantidade que queremos remover
            if getattr(item, 'quantity', 1) > amount:
                item.quantity -= amount
                print(f"[-] {entity.name} consumiu {amount}x {item.name}. Restam {item.quantity}.")
                return True
            else:
                entity.inventory.remove(item)
                if item.stackable:
                # Se a quantidade for igual ou menor, removemos o slot inteiro
                    print(f"[-] {entity.name} esgotou o estoque de {item.name}.")
                else:
                    print(f"[-] {entity.name} usou o {item.name}.")
                return True

        @staticmethod
        def has_item_by_id(entity, target_id: str) -> bool:
            """Verifica se o item existe, independente da quantidade."""
            inventory = getattr(entity, 'inventory', [])
            return any(item.id == target_id for item in inventory)

        @staticmethod
        def get_item_by_id(entity, target_id: str) -> Optional[Item]:
            """Retorna o objeto do item (que agora contém a quantidade total)."""
            inventory = getattr(entity, 'inventory', [])
            return next((item for item in inventory if item.id == target_id), None)