from src.engine.game_state import GameState
from src.handlers.inventory_handler import InventoryHandler
from src.handlers.xp_handler import LevelHandler
from src.models.database.item_db import ItemDB
from src.models.entities.scene import GameScene, SceneOption
from src.services.sanity_service import SanityService


def description_gates(player):
    msg = ("O Sanatório de Gray Fields surge da névoa como um gigante de concreto e ferro em decomposição.\n"
          "O portão principal, uma estrutura de ferro batido de quatro metros de altura, está selado não por cadeados,\n"
          "mas por uma crosta de mofo cinzento que parece ter soldado as engrenagens.\n")
    msg += ("\nO ar é carregado de partículas em suspensão que brilham fracamente sob a luz da sua lamparina.\n"
            "Você ouve o estalo do metal contraindo pelo frio, mas há um som dissonante: um silvo rítmico vindo debaixo da terra.\n"
            "Tubulações de cobre esverdeado emergem do solo e correm pelas paredes externas, vibrando com a passagem de algo sob alta pressão.\n")
    msg += ("\nUm aviso pregado na guarita lateral, corroído pela umidade, ainda é legível: 'SETOR DE MANUTENÇÃO: NÃO DESLIGUE O FLUXO DE VAPOR. O CALOR RETARDA A ESPALHA.'\n"
            "Miller não estava delirando nas cartas; o sistema de caldeiras é o que mantém este lugar minimamente seguro.")
    return msg

def try_force_gate(player):
    if not InventoryHandler.has_item_by_id(player, "pe_de_cabra"):
        SanityService.reduce_sanity(player, 5)
        return ("\nVocê tenta empurrar o metal, mas as mãos afundam na massa cinzenta do mofo.\n"
                "A substância é fria e pulsa contra sua pele. Um pânico instintivo te faz recuar.")

    return ("\nVocê usa o Pé de Cabra, mas o metal nem se mexe. A 'solda' de mofo é mais forte que o ferro.\n"
            "O esforço apenas faz com que uma nuvem de esporos suba. Melhor não insistir aqui.")


def search_guardhouse(player):
    if GameState.get("guardhouse_looted"):
        return "\nA guarita está revirada. Apenas papéis úmidos e o cheiro de ozônio restaram."

    msg = "\nVocê entra na guarita. O vidro da janela foi quebrado de dentro para fora..\n"
    msg += "No chão, sob uma camada de poeira, você encontra uma chave de latão com uma etiqueta: 'CALDEIRA SETOR 02'.\n"

    key = ItemDB.get_item("chave_vapor")
    InventoryHandler.add_item(player, key)
    GameState.set("guardhouse_looted", True)

    return msg + "\nVocê sente que está sendo observado pelas janelas do andar superior do Sanatório."


def analyze_mold_pattern(player):
    msg = "\nVocê se aproxima da base do muro, mantendo uma distância segura das crostas.\n"
    msg += "O mofo cinza não é apenas um fungo; ele se organiza em padrões fractais, quase geométricos.\n"
    msg += "Onde o vapor vaza, o mofo murcha e se torna uma fuligem preta inofensiva."

    if not GameState.get("learned_steam_weakness"):
        GameState.set("learned_steam_weakness", True)
        msg += "\n💡 O calor intenso neutraliza a integridade estrutural do mofo."
        LevelHandler.earn_xp(player, 2)

    return msg

def follow_heat_path(player):
    msg = ("Você se afasta da inércia gelada dos portões e começa a ladear o muro de contenção,\n"
           "guiado pelo zumbido grave que emana do solo. O frio cortante do vale\n"
           "dá lugar a uma umidade pesada e sufocante.\n")

    msg += ("\nAs tubulações de cobre vibram sob sua palma. O mofo aqui é ralo, incapaz de fincar raízes.\n"
            "Ao dobrar a esquina, você encontra uma porta de serviço maciça com a trava solta.\n"
            "O vapor escapa pelas frestas com um silvo ensurdecedor.\n")

    if player.sanity < 50:
        player.sanity += 15
        msg += "\n💡 O calor intenso acalma seus tremores. O mofo não o seguirá aqui dentro.\n"

    msg += "\nVocê empurra o aço pesado. Uma lufada de ar quente te atinge quando você entra..."

    if player.sanity < 50:
        player.sanity += 15
        msg += "\n\n💡 O calor intenso acalma seus tremores. O mofo não o seguirá aqui dentro."

    return msg

SANATORIUM_GATES = GameScene(
    id="sanatorium_gates",
    title="Os Portões do Sanatório",
    description=description_gates,
    options=[
        SceneOption("Seguir o fluxo de calor das tubulações", action=follow_heat_path, requirement=lambda p: GameState.get("guardhouse_looted"), target_scene_id="steam_room"),
        SceneOption("Analisar o padrão de crescimento do mofo nos muros", action=analyze_mold_pattern, target_scene_id="sanatorium_gates"),
        SceneOption("Vasculhar a Guarita de Segurança", action=search_guardhouse, target_scene_id="sanatorium_gates"),
        SceneOption("Tentar forçar a abertura dos portões", action=try_force_gate, target_scene_id="sanatorium_gates"),
        SceneOption("Retornar ao Grande Campo da Névoa", target_scene_id="sanatorium_fields")
    ]
)