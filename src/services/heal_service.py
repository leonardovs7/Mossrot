from src.handlers.inventory_handler import InventoryHandler


class HealService:
    @staticmethod
    def heal(player, item) -> str:
        """
        Aplica a cura ao player e gerencia o consumo do item.
        """
        # 1. Verificação de categoria (segurança extra)
        if item.category != "heal":
            return f"O {item.name} não tem propriedades curativas."

        # 2. Lógica de cura (usando o min para não estourar o max_hp)
        old_hp = player.hp
        player.hp = min(player.max_hp, player.hp + item.value)
        recuperado = player.hp - old_hp

        # 3. Consumo do item (Aqui estava o detalhe!)
        # Precisamos passar (player, item) para o Handler saber qual mochila abrir
        if item.is_consumable:
            InventoryHandler.remove_item(player, item)

        # 4. Feedback narrativo
        if recuperado == 0:
            return f"Você ingere {item.name}, mas suas feridas já parecem estar o mais fechadas possível. (HP: {player.hp}/{player.max_hp})"

        return (f"Você ingere {item.name} e sente o calor da vida retornando..."
                f"❤️ HP: {player.hp}/{player.max_hp} (+{recuperado})")