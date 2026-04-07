import time

from src.engine.game_state import GameState
from src.handlers.inventory_handler import InventoryHandler
from src.models.database.item_db import ItemDB
from src.models.entities.enemy import Enemy
from src.models.entities.scene import GameScene, SceneOption
from src.services.combat_service import CombatService


def on_enter_basement(player):
    if GameState.get("half_corpse_defeated"):
        return

    print("\nVocê termina de subir os últimos degraus e o cheiro de cobre atinge suas narinas como um soco.")
    time.sleep(1.5)

    # Descrição visceral do evento
    print("O assoalho de madeira range. No canto escuro, sob uma mesa de necrotério, algo se debate.")
    print("Um som úmido ecoa enquanto algo se arrasta com uma velocidade antinatural.")
    time.sleep(2)

    print("\n⚠️  DE REPENTE, A LUZ DA SUA CHAMA REVELA O HORROR!")
    print("É o que restou do Vigia. Ele está partido ao meio na altura da cintura, "
          "seus intestinos se arrastam atrás dele como caudas de rato cinzentas.")
    print("Com um grito rouco e sem pulmões, ele se lança contra suas pernas, "
          "usando as mãos em carne viva para se impulsionar!")
    time.sleep(1)

    half_corpse = Enemy(name="Vigia Desmembrado", level=player.level, hp=1, max_hp=1, base_damage=5, damage_reduction=0.0, xp_reward=5)
    CombatService.start_combat(player, half_corpse, is_surprise=True)

    if player.is_alive:
        GameState.set("half_corpse_defeated", True)
        return ("\nO tronco do homem para de se debater sob seus pés. "
              "O silêncio volta a reinar, quebrado apenas pelo gotejar do sangue entre as tábuas do chão.")

def pry_open_files(player):
    if not InventoryHandler.has_item_by_id(player, "pe_de_cabra"):
        return "❌ A gaveta de aço está emperrada pelo tempo. Você precisa de algo para alavancá-la."

    if GameState.get("files_opened"):
        return "\nA gaveta já está aberta e vazia."

    GameState.set("files_opened", True)
    # Adiciona um item de lore ou mapa
    return (
        "\n*CRACK!* Você força o metal com o Pé de Cabra Ensanguentado. Dentro, há fichas de óbito.\n"
        "Todas as fichas têm a mesma causa da morte: 'Rejeição Tecidual Externa'.\n"
        "Você encontra um 'Esboço da Lavanderia' que revela uma entrada lateral secreta."
    )

def discover_hidden_stash(player):
    # Só funciona se o foco estiver ativo
    item = ItemDB.get_item("tintura_de_opio") # Um consumível de Sanidade
    InventoryHandler.add_item(player, item)
    return (
        "\n👁️ Sob a luz do Âmbar, você vê que as tábuas do chão não batem com o resto.\n"
        "Você move um tapete de pele de lobo mofado e encontra um compartimento secreto.\n"
        "Lá dentro, o Vigia escondia 'Tintura de Ópio' para suportar o que via nas lentes."
    )

def scavenge_watcher_tools(player):
    if not InventoryHandler.has_item_by_id(player, "pe_de_cabra"):
        item = ItemDB.get_item("pe_de_cabra")
        InventoryHandler.add_item(player, item)
        return (
            "\nSob uma lâmpada oscilante, você encontra o Pé de Cabra sobre uma mesa de metal limpa.\n"
            "Ele brilha sob a luz da sua chama, mas o ferro está batizado com crostas de sangue\n"
            "que parecem ter escorrido de um impacto recente. O peso dele em sua mão é reconfortante,\n"
            "mas o cheiro metálico de sangue fresco que ainda emana do metal te faz olhar para as sombras."
        )
    return "\nA mesa de ferramentas está vazia, restando apenas o contorno de onde o pé de cabra estava."


def scavenge_meds(player):
    """Vasculha o armário em busca de suprimentos médicos padrão."""

    # Verificação de coleta única
    if GameState.get("watcher_meds_taken"):
        return "\nVocê olha para o armário de metal, mas as prateleiras estão limpas de qualquer utilidade."

    item = ItemDB.get_item("sais_clinicos")

    if item:
        InventoryHandler.add_item(player, item)
        GameState.set("watcher_meds_taken", True)

        # Construindo a mensagem
        msg = "\nVocê abre a porta rangente do armário de primeiros socorros.\n"
        msg += "O interior está manchado de iodo e mofo, mas um frasco lacrado brilha no fundo.\n"

        msg += f"\nVocê encontrou: {item.name}.\n"

        msg += "\nO cheiro forte que escapa da tampa mal vedada faz seus olhos lacrimejarem, "
        msg += "mas traz uma clareza súbita e necessária para quem caminha no abismo.\n"

        msg += "💡 O frasco contém doses suficientes para restaurar sua Vida e sua Sanidade."

        return msg

    return "\nO armário contém apenas agulhas tortas e gaze ensanguentada inútil."

WATCHER_BASEMENT = GameScene(
    id = "watcher_basement",
    title="O Porão do Observador",
    description="Você emerge em um porão atulhado de estantes que gemem sob o peso de frascos de vidro.\n"
        "Dentro deles, órgãos preservados em líquido turvo parecem pulsar quando você não está olhando.\n"
        "Uma mesa de carvalho no centro está coberta por mapas topográficos do vale, onde o Sanatório\n"
        "está marcado com círculos vermelhos agressivos. Binóculos pesados e tripés de câmera apontam\n"
        "para pequenas frestas nas janelas de sótão, direcionadas para a silhueta imponente do complexo\n"
        "de Vidro Fosco no horizonte.\n\n"
        "O dono desta casa não olhava para o campo para protegê-lo, mas para catalogar o que escapava de lá.",
    on_enter=on_enter_basement,
    on_enter_repeatable=False,
    options=[
        SceneOption("Segredo: Vasculhar o compartimento sob o tapete",
                    requirement=lambda p: GameState.get("focus_active"),
                    action=discover_hidden_stash,
                    target_scene_id="watcher_basement"),
        SceneOption("Investigar a mesa de necrotério", action=scavenge_watcher_tools, only_once=True, target_scene_id="watcher_basement"),
        SceneOption("Vasculhar o armário de remédios roubados", action=scavenge_meds, only_once=True, target_scene_id="watcher_basement"),
        SceneOption("Forçar gaveta de arquivos", action=pry_open_files, target_scene_id="watcher_basement"),
        SceneOption("Subir para o andar de cima", target_scene_id="watcher_living_room"),
        SceneOption("Descer de volta para o Nexo", target_scene_id="abism_third_chamber")
    ]
)