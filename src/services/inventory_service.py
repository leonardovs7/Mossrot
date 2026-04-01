from src.handlers.inventory_handler import InventoryHandler
from src.services.heal_service import HealService
from src.services.light_service import LightService
from src.services.weapon_armor_service import WeaponArmorService


class InventoryService:
    @staticmethod
    def use(player, item) -> str:
        """
        O 'Maestro' do uso de itens.
        Decide qual serviço chamar e devolve a mensagem de feedback.
        """

        # 1. Itens de Consumo (Cura)
        if item.category == "heal":
            return HealService.heal(player, item)

        # 2. Itens de Utilidade (Luz/Sanidade)
        if item.category == "light":
            return LightService.light_up(player, item)

        # 3. Equipamentos (Armas e Armaduras)
        if item.category == "weapon":
            return WeaponArmorService.equip_weapon(player, item)

        if item.category == "armor":
            return WeaponArmorService.equip_armor(player, item)

        # 4. Caso o item não tenha uma função implementada
        return f"Você observa o {item.name}, mas não sabe como usá-lo agora..."
