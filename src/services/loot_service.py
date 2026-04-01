import random
from src.handlers.inventory_handler import InventoryHandler
from src.models.entities.item import Item

class LootService:
    @staticmethod
    def check_loot(player) -> str:
        drop_chance = 0.4

        if random.random() < drop_chance:
            item_id = random.choice(["cura_leve", "oleo_carne"])

            if item_id == "cura_leve":
                novo_item = Item(id="cura_leve", name="Tônico de Seiva Amarga", category="heal", value=5)
            else:
                novo_item = Item(id="oleo_carne", name="Óleo de Carne Velha", category="fuel", value=20)

            InventoryHandler.add_item(player, novo_item)

            return f"✨ Você vasculha os restos e encontra: **{novo_item.name}**!"

        return "🌑 Você vasculha as cinzas, mas a escuridão não deixou nada para trás."