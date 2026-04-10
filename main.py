import sys

from src.engine.game_state import GameState
from src.engine.scene_bridge import SceneBridge
from src.engine.scene_manager import SceneManager
from src.models.database.scenes_db import ALL_SCENES
from src.models.entities.player import Player

def main():
    GameState.set("active", True)

    SceneBridge.say("Você desperta na terra fria de uma floresta densa e sombria, a mente turva e sem memória de como chegou ali..")
    SceneBridge.say("\nComo a história chamará você? ")
    nome = input("> ")
    if not nome.strip():
        SceneBridge.say("\nCertas memórias insistem porque as culpas por trás delas nunca cessaram.")
        nome = "Desolado"
    player = Player(name=nome)
    SceneBridge.say(f"Você será chamado de {player.name}.")
    input("\n[Pressione Enter para continuar...]")

    try:
        manager = SceneManager(scenes=ALL_SCENES, start_id="dense_florest")
        manager.navigate(player)

    except KeyboardInterrupt:
        print("\n\nSaindo do pesadelo... Sua corrupção foi pausada.")
        sys.exit()
    except Exception as e:
        print(f"\nErro: {e}")

if __name__ == "__main__":
    main()