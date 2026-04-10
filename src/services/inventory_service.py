from src.engine.game_state import GameState
from src.handlers.inventory_handler import InventoryHandler
from src.services.heal_service import HealService
from src.services.light_service import LightService
from src.services.sanity_service import SanityService


class WeaponArmorService:

    @staticmethod
    def equip_weapon(player, item) -> str:
        if item.category != "weapon":
            return f"❌ {item.name} não possui o peso de uma arma."

        feedback = ""

        # 2. Lógica de Troca (Swap)
        if hasattr(player, 'equipped_weapon') and player.equipped_weapon:
            old_weapon = player.equipped_weapon
            InventoryHandler.add_item(player, old_weapon)
            feedback = f"Você guardou {old_weapon.name}. "

        # 3. Substituição de Valores
        player.equipped_weapon = item
        player.weapon = item.name
        player.base_damage = player.base_damage + item.value
        player.current_weapon_damage = item.value
        player.current_weapon_bonus = item.passive_bonus

        # 4. Remove a arma nova da mochila
        InventoryHandler.remove_item(player, item)

        return feedback + f"Você agora empunha {item.name}. (Dano: +{item.value})"

    @staticmethod
    def equip_armor(player, item) -> str:
        # 1. Validação
        if item.category != "armor":
            return f"❌ {item.name} não serve como proteção."

        feedback = ""

        # 2. Lógica de Troca
        if hasattr(player, 'equipped_armor') and player.equipped_armor:
            old_armor = player.equipped_armor
            InventoryHandler.add_item(player, old_armor)
            feedback = f"Você removeu {old_armor.name}. "

        # 3. Substituição de Valores
        player.equipped_armor = item
        player.armor = item.name
        player.damage_reduction = player.damage_reduction + item.value
        player.current_armor_defense = item.value
        player.current_armor_bonus = item.passive_bonus

        # 4. Remove da mochila
        InventoryHandler.remove_item(player, item)
        percent = int(player.current_armor_defense * 100)

        return feedback + f"Você vestiu {item.name}. (Defesa: +{percent}%)"

class InventoryService:
    @staticmethod
    def use(player, item) -> str:
        """
        O 'Maestro' do uso de itens.
        Decide qual serviço chamar e devolve a mensagem de feedback.
        """

        # 1. Itens de Consumo (Cura)
        if item.category == "heal" and not item.subcategory == "sanityHeal" and not item.subcategory == "multiHeal":
            return HealService.heal(player, item)

        # 1.1 Itens de Consumo (Sanidade)
        if item.category == "heal" and item.subcategory == "sanityHeal":
            return SanityService.increase_sanity(player, item.value)

        # 1.2 Itens de Consumo com buff múltiplo
        if item.subcategory == "multiHeal":
            return f"{SanityService.increase_sanity(player, item.value)} \nAlém disso, {HealService.heal(player, item).lower()}"

        # 2. Itens de Utilidade (Luz/Sanidade)
        if item.category == "light":
            return LightService.light_up(player, item)

        if item.category == "fuel":
            return LightService.refuel(player, item)

        # 3. Equipamentos (Armas e Armaduras)
        if item.category == "weapon":
            return WeaponArmorService.equip_weapon(player, item)

        if item.category == "armor":
            return WeaponArmorService.equip_armor(player, item)

        # 4. Item de Visualização
        if item.category == "view":
            if not GameState.get("focus_active"):
                GameState.set("focus_active", True)
                return ("Você ergue o Âmbar. A realidade se dobra, revelando o fluxo da seiva negra nas paredes."
                        "\n> Novas Opções Liberadas!")
            return "Você já está concentrado e enxergando mais do que deveria ser possível ver.."

        # 5. Caso o item não tenha uma função implementada
        return f"Você observa o {item.name}, mas não sabe como usá-lo agora..."