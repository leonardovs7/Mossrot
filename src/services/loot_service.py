import random
import time

from src.handlers.inventory_handler import InventoryHandler
from src.models.database.item_db import ItemDB
from src.models.entities.item import Item

class LootService:
    @staticmethod
    def check_loot(player) -> str:
        drop_chance = 0.4

        if random.random() < drop_chance:
            item_id = random.choice(["tonico_amargo", "oleo_carne"])

            novo_item = ItemDB.get_item(item_id)

            if novo_item:
                InventoryHandler.add_item(player, novo_item)
                return f"\n✨ Você vasculha os restos e encontra: {novo_item.name}!"

            return f"\n⚠️ Algo caiu, mas o ID '{item_id}' não foi achado no ItemDB."

        return "\nVocê vasculha as cinzas, mas a escuridão não deixou nada para trás."