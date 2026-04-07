import time

from src.handlers.inventory_handler import InventoryHandler
from src.models.entities.item import LightEquipment


class LightService:

    @staticmethod
    def light_up(player, item) -> str:
        # 1. Validação do item
        if not hasattr(item, 'is_lit'):
            return "Este item não emite luz."

        # 2. Lógica de "Toggle" (Ligar/Desligar)
        if not item.is_lit:
            if item.fuel <= 0:
                return f"⚠️ A {item.name} está seca. Você precisa de combustível."

            item.is_lit = True
            player.has_light = True
            # Recupera sanidade (limitado ao máximo)
            player.sanity = min(player.max_sanity, player.sanity + item.value)

            tipo_chama = "rápida" if item.is_consumable else "pálida"
            return (f"\nA chama {tipo_chama} da {item.name} estala, revelando silhuetas.\n"
                    f"> Combustível: {item.fuel:.1f}/{item.max_fuel}\n"
                    f"> Sanidade: {player.sanity}/{player.max_sanity} (+{item.value})")

        else:
            item.is_lit = False
            player.has_light = False
            return f">> Você apaga a {item.name} para poupar combustível."

    @staticmethod
    def process_consume(player) -> list:
        """
        Deve ser chamado a cada movimento ou turno no SceneManager.
        """
        feedback_messages = []

        for item in player.inventory:
            # Só consome se for um equipamento de luz e estiver ACESO
            if hasattr(item, 'fuel') and getattr(item, 'is_lit', False):
                # 1. Consumo fixo ou percentual
                item.fuel = max(0.0, item.fuel - item.fuel_consume)

                # 2. Alertas de nível baixo
                if 0 < item.fuel <= 10:
                    feedback_messages.append(f"\n⚠️ A chama da {item.name} vacila. Está no fim!")
                    time.sleep(2)

                # 3. Apagar automático
                if item.fuel == 0:
                    item.is_lit = False
                    player.has_light = False
                    feedback_messages.append(f"\n🌑 A {item.name} se apagou! A escuridão te envolve.")

        return feedback_messages

    @staticmethod
    def refuel(player, fuel_item) -> str:
        if fuel_item.category != "fuel":
            return "Isso não serve para abastecer."

        # 1. Trava do Fósforo (Check de segurança)
        if not InventoryHandler.has_item_by_id(player, "caixa_fosforos"):
            return "⚠️ Você precisa de fósforos para manipular o óleo com segurança."

        # 2. Busca a fonte de luz no inventário
        light_item = next((i for i in player.inventory if i.category == "light"), None)

        if not light_item:
            return "❌ Você não tem nada para abastecer."

        # 3. Aplicação do Combustível
        old_fuel = light_item.fuel
        light_item.fuel = min(light_item.max_fuel, light_item.fuel + fuel_item.value)
        gain = light_item.fuel - old_fuel

        feedback = f"✨ Você abastece a {light_item.name}. [+{gain:.1f} de combustível]"

        # 4. Re-acendimento automático
        if not light_item.is_lit:
            light_item.is_lit = True
            player.has_light = True
            feedback += "\n🔥 Você risca um fósforo e reacende a chama."

        # 5. Consome o item de combustível da mochila
        InventoryHandler.remove_item(player, fuel_item)
        return feedback

    @staticmethod
    def force_relight(player, fuelAmount: float = 30.0):
        # Busca a lamparina no inventário
        light_item = next((i for i in player.inventory if isinstance(i, LightEquipment)), None)

        if light_item:
            light_item.fuel = fuelAmount
            light_item.is_lit = True
            player.has_light = True
            return f">> A {light_item.name} brilha novamente! [+{fuelAmount} de combustível]"
        return "Você não possui uma fonte de luz para reacender."
