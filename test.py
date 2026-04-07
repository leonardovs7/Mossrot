import sys

from src.engine.game_state import GameState
from src.engine.scene_manager import SceneManager
from src.handlers.inventory_handler import InventoryHandler
from src.models.database.item_db import ItemDB
from src.models.database.scenes_db import ALL_SCENES
from src.models.entities.player import Player
from src.services.inventory_service import InventoryService


def main():
    GameState.set("active", True)

    print("Você desperta na terra fria de uma floresta densa e sombria, a mente turva e sem memória de como chegou ali..")
    print("\nComo a história chamará você? ")
    nome = input("> ")
    if not nome.strip():
        print("\nCertas memórias insistem porque as culpas por trás delas nunca cessaram.")
        nome = "Desolado"
    player = Player(name=nome)
    print(f"Você será chamado de {player.name}.")
    input("\n[Pressione Enter para continuar...]")

    InventoryHandler.add_item(player, ItemDB.get_item("lamparina_musgosa"))
    InventoryHandler.add_item(player, ItemDB.get_item("caixa_fosforos"))
    InventoryHandler.add_item(player, ItemDB.get_item("oleo_carne"))
    InventoryHandler.add_item(player, ItemDB.get_item("cicatriz_ambar"))
    player.hp = 4000
    player.max_hp = 4000
    player.base_damage = 300


    try:
        manager = SceneManager(scenes=ALL_SCENES, start_id="watcher_basement")
        manager.navigate(player)

    except KeyboardInterrupt:
        print("\n\nSaindo do pesadelo... Sua corrupção foi pausada.")
        sys.exit()
    except Exception as e:
        print(f"\nErro: {e}")

if __name__ == "__main__":
    main()