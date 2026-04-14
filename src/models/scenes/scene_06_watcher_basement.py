import time

from src.engine.game_state import GameState
from src.handlers.inventory_handler import InventoryHandler
from src.handlers.xp_handler import LevelHandler
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
    print("O assoalho de madeira range. No canto escuro, sob uma bancade de marcenaria, algo se debate.")
    print("Um som úmido ecoa enquanto algo se arrasta com uma velocidade antinatural.")
    time.sleep(2)

    print("\nDE REPENTE, A LUZ DA SUA CHAMA REVELA O HORROR!\n")
    print("É o que restou do Vigia. Ele está partido ao meio na altura da cintura, "
          "seus intestinos se arrastam atrás dele como caudas de rato cinzentas.")
    print("Com um grito rouco e sem pulmões, ele se lança contra suas pernas, "
          "usando as mãos em carne viva para se impulsionar!\n")
    time.sleep(1)

    half_corpse = Enemy(name="Vigia Desmembrado", level=player.level, hp=1, max_hp=1, base_damage=5, damage_reduction=0.0, xp_reward=5)
    CombatService.start_combat(player, half_corpse, is_surprise=True)

    if player.is_alive:
        GameState.set("half_corpse_defeated", True)
        print(("\nO tronco do homem para de se debater sob seus pés. "
              "O silêncio volta a reinar, quebrado apenas pelo gotejar do sangue entre as tábuas do chão."))
        return "watcher_basement"

def pry_open_files(player):
    if not InventoryHandler.has_item_by_id(player, "pe_de_cabra"):
        return "A gaveta de aço está emperrada pelo tempo. Você precisa de algo para alavancá-la."

    if GameState.get("files_opened"):
        return "\nA gaveta já está aberta e vazia."

    GameState.set("files_opened", True)
    msg = "*CRACK!* O metal cede. Você não encontra relatórios, mas sim um diário de vigilância.\n"
    msg += "As páginas estão cheias de horários e desenhos feitos à mão, trêmulos e obsessivos.\n"

    msg += "\n--- 👁️ REGISTROS DO VIGIA ---\n"
    msg += "> '03:14 AM - As luzes da Ala Oeste não apagam mais. Vi o vulto de novo. \n"
    msg += "> Ele não caminha, ele desliza. Como se estivesse preso ao teto por fios invisíveis.'\n"

    msg += "\n> 'Eles trouxeram as caixas de novo. Caixas compridas, pesadas demais para remédios. \n"
    msg += "> O cheiro que sai delas atravessa o pátio e chega até minha janela. Cheiro de terra molhada e... algo doce.'\n"

    msg += "\n> 'Alguém me viu hoje. Uma silhueta na janela da Lavanderia. \n"
    msg += "> Ficou lá por horas, apenas me encarando. Eu não vi olhos, vi apenas dois furos negros.'\n"

    msg += "\nNo canto da última página, há um lembrete circulado várias vezes:\n"
    msg += "'Não use o portão principal. Eles soldaram as trancas por um motivo. Entre por onde o vapor sai.'"

    msg += "\n\nO Vigia parecia aterrorizado com o que via na Lavanderia, mas apontou aquele lugar como a única entrada."

    LevelHandler.earn_xp(player, 5)
    return msg

def discover_hidden_stash(player):
    # Só funciona se o foco estiver ativo
    item = ItemDB.get_item("tonico_opio") # Um consumível de Sanidade
    InventoryHandler.add_item(player, item)
    return (
        "\n👁️ Sob a luz do Âmbar, você vê que as tábuas do chão não batem com o resto.\n"
        "Você move um tapete de pele de lobo mofado e encontra um compartimento secreto.\n"
        "Lá dentro, o Vigia escondia 'Tônico de Ópio' para suportar o que via nas lentes."
    )

def scavenge_watcher_tools(player):
    if not InventoryHandler.has_item_by_id(player, "pe_de_cabra"):
        item = ItemDB.get_item("pe_de_cabra")
        InventoryHandler.add_item(player, item)
        return (
            "\nSob uma lâmpada oscilante, você encontra o Pé de Cabra entre prensas de madeira e bandejas de ácido para fotos.\n"
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
    description="Você emerge em um porão atulhado de estantes que gemem sob o peso de frascos de conserva.\n"
        "Dentro deles, fibras escuras e tecidos que lembram raízes humanas parecem pulsar em fluido turvo.\n"
        "Uma bancada de carvalho rústico no centro está coberta por mapas topográficos do vale, \n"
        "onde o Sanatório está marcado com círculos vermelhos agressivos. \n\n"
        "Binóculos pesados e tripés de câmera apontam para frestas nas janelas de sótão, \n"
        "direcionadas para a silhueta imponente do complexo de Vidro Fosco no horizonte.\n"
        "O dono desta casa não olhava para o campo para protegê-lo, mas para catalogar o que escapava de lá.",
    on_enter=on_enter_basement,
    on_enter_repeatable=False,
    options=[
        SceneOption("Segredo: Vasculhar a saliência oca sob o tapete apodrecido",
                    requirement=lambda p: GameState.get("focus_active"),
                    action=discover_hidden_stash,
                    only_once=True,
                    target_scene_id="watcher_basement"),
        SceneOption("Remexer as vísceras de metal na bancada de trabalho", action=scavenge_watcher_tools, only_once=True, target_scene_id="watcher_basement"),
        SceneOption("Vasculhar o estoque de frascos e remédios surrupiados", action=scavenge_meds, only_once=True, target_scene_id="watcher_basement"),
        SceneOption("Forçar a trava emperrada da gaveta de arquivos", action=pry_open_files, target_scene_id="watcher_basement"),
        SceneOption("Ascender rumo ao andar de cima", target_scene_id="watcher_living_room"),
        SceneOption("Mergulhar de volta no abismo do Nexo", target_scene_id="abism_third_chamber")
    ]
)