from src.engine.game_state import GameState
from src.handlers.inventory_handler import InventoryHandler
from src.models.database.item_db import ItemDB
from src.services.heal_service import HealService
from src.services.light_service import LightService
from src.services.sanity_service import SanityService
from src.models.enums import ItemCategory, ItemSubcategory


class WeaponArmorService:

    @staticmethod
    def equip_weapon(player, item) -> str:
        # Validação usando Enum
        if item.category != ItemCategory.WEAPON:
            return f"❌ {item.name} não possui o peso de uma arma."

        feedback = ""

        # Lógica de Troca (Swap)
        if hasattr(player, 'equipped_weapon') and player.equipped_weapon:
            old_weapon = player.equipped_weapon
            InventoryHandler.add_item(player, old_weapon)
            feedback = f"Você guardou {old_weapon.name}. "

        # Substituição de Valores
        player.equipped_weapon = item
        player.weapon = item.name
        player.base_damage = player.base_damage + item.value
        player.current_weapon_damage = item.value
        player.current_weapon_bonus = item.passive_bonus

        InventoryHandler.remove_item(player, item)

        return feedback + f"Você agora empunha {item.name}. (Dano: +{item.value})"

    @staticmethod
    def equip_armor(player, item) -> str:
        # Validação usando Enum
        if item.category != ItemCategory.ARMOR:
            return f"❌ {item.name} não serve como proteção."

        feedback = ""

        # Lógica de Troca
        if hasattr(player, 'equipped_armor') and player.equipped_armor:
            old_armor = player.equipped_armor
            InventoryHandler.add_item(player, old_armor)
            feedback = f"Você removeu {old_armor.name}. "

        # Substituição de Valores
        player.equipped_armor = item
        player.armor = item.name
        player.damage_reduction = player.damage_reduction + item.value
        player.current_armor_defense = item.value
        player.current_armor_bonus = item.passive_bonus

        InventoryHandler.remove_item(player, item)
        percent = int(player.current_armor_defense * 100)

        return feedback + f"Você vestiu {item.name}. (Defesa: +{percent}%)"


class InventoryService:
    @staticmethod
    def use(player, item) -> str:
        """
        O 'Maestro' do uso de itens utilizando match/case para categorias e subcategorias.
        """
        if isinstance(item, str):
            item_id = item
            item = ItemDB.get_item(item_id)

            if not item:
                return f"❌ Erro sistêmico: O item '{item_id}' não foi encontrado no banco de dados."

        # O Maestro entra em cena
        match item.category:

            case ItemCategory.HEAL:
                # Se for HYBRID (HP + Sanidade), processa ambos
                if item.subcategory == ItemSubcategory.HYBRID:
                    res_sanity = SanityService.increase_sanity(player, item.value)
                    res_heal = HealService.heal(player, item)
                    return f"{res_sanity} \nAlém disso, {res_heal.lower()}"

                # Se for STANDARD, apenas cura HP
                return HealService.heal(player, item)

            case ItemCategory.SANITY:
                return SanityService.increase_sanity(player, item.value)

            case ItemCategory.LIGHT:
                return LightService.light_up(player, item)

            case ItemCategory.FUEL:
                return LightService.refuel(player, item)

            case ItemCategory.WEAPON:
                return WeaponArmorService.equip_weapon(player, item)

            case ItemCategory.ARMOR:
                return WeaponArmorService.equip_armor(player, item)

            case ItemCategory.VIEW:
                if item.subcategory == ItemSubcategory.UNIQUE:
                    if not GameState.get("focus_active"):
                        GameState.set("focus_active", True, immutable=False)
                        return (
                            "Você ergue o Âmbar. A realidade se dobra, revelando o fluxo da seiva negra nas paredes."
                            "\n> Novas Opções Liberadas!")
                    return "Você já está concentrado e enxergando mais do que deveria ser possível ver.."
                return f"Você observa o {item.name}, mas nada acontece."

            case _:
                # Engloba KEY, LORE e qualquer outra coisa sem uso ativo
                return f"Você observa o {item.name}, mas não sabe como usá-lo agora..."