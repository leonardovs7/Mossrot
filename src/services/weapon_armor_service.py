# src/services/weapon_armor_service.py
from src.handlers.inventory_handler import InventoryHandler

class WeaponArmorService:

    @staticmethod
    def equip_weapon(player, item):
        # 1. Validação
        if item.category != "weapon": # Certifique-se que no seu JSON está em minúsculo
            return f"❌ {item.name} não pode ser empunhado como arma."

        # Guardamos o poder TOTAL que o player tinha antes da troca
        old_power = player.total_damage

        # 2. Lógica de Troca (Swap)
        if player.equipped_weapon:
            InventoryHandler.add_item(player, player.equipped_weapon)
            old_weapon_name = player.equipped_weapon.name
        else:
            old_weapon_name = "Mãos Machucadas"

        # 3. Equipar e remover da mochila
        player.equipped_weapon = item
        InventoryHandler.remove_item(player, item)

        # 4. Feedback usando a @property total_damage
        return (f"\n[ARMA EQUIPADA!] - 🗡️\n"
                f"Você guardou {old_weapon_name} e sacou {item.name}.\n"
                f"(Dano Anterior: {old_power} | Dano Atual: {player.total_damage})")

    @staticmethod
    def equip_armor(player, item):
        # 1. Validação
        if item.category != "armor":
            return f"❌ {item.name} não pode ser usado como armadura."

        # Guardamos a redução TOTAL de antes
        old_reduction = player.total_reduction

        # 2. Lógica de Troca
        if player.equipped_armor:
            InventoryHandler.add_item(player, player.equipped_armor)
            old_armor_name = player.equipped_armor.name
        else:
            old_armor_name = "Roupas Rasgadas"

        # 3. Equipar e remover da mochila
        player.equipped_armor = item
        InventoryHandler.remove_item(player, item)

        # 4. Feedback usando a @property total_reduction
        return (f"\n[ARMADURA EQUIPADA!] - 🛡️\n"
                f"Você guardou {old_armor_name} e sacou {item.name}.\n"
                f"(Defesa Anterior: {old_reduction} | Defesa Atual: {player.total_reduction})")