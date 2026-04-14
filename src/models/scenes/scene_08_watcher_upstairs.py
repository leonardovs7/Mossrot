from src.handlers.inventory_handler import InventoryHandler
from src.models.database.item_db import ItemDB
from src.models.entities.scene import GameScene, SceneOption
from src.models.enums import SceneType


def cut_pillow(player):
    print("\nVocê usa sua lâmina para cortar as fibras negras que protegem o ninho.\n"
          "No centro do colchão apodrecido, você encontra o que restou de uma pessoa... e um Amolador de Pedra Negra.")
    player.base_damage += 2
    if player.equipped_weapon != "Mãos Machucadas":
        print("Você esfrega a pedra contra o que usa para sobreviver..\n"
                    "A pedra consome a sua pele, deixando um rastro de cinzas escuras que se infiltram sob suas unhas e cicatrizes.")
        return "\n[BÔNUS: Seu dano aumentou permanentemente em 2 pontos!]"
    print("\nVocê esfrega a pedra contra o que usa para sobreviver.. O metal solta faíscas negras e secas.\n"
          "Conforme a pedra se desintegra em uma poeira fina e escura, você sente um peso novo em seus gestos.\n"
          "Sua intenção de ferir tornou-se mais afiada, mais precisa.")
    return "\n[BÔNUS: Seu dano aumentou permanentemente em 2 pontos!]"

def see_bedside_table(player):
    print("\nA madeira está deformada pela umidade, mas cede com um estalo.\n"
          "Entre papéis em branco e restos de insetos, você encontra uma pasta avermelhada que parece pulsar levemente.\n")
    return InventoryHandler.add_item(player, ItemDB.get_item("unguento_fibroso"))

def investigate_closet(player):
    if InventoryHandler.has_item_by_id(player, "estilete_raiz"):
        return ("\nAs gavinhas se retraem com um chiado, reconhecendo a lâmina em sua mão. "
               "As portas se abrem sem resistência.")
    player.hp = max(1, player.hp - 1)
    return ("\nVocê força as portas, sentindo as farpas rasgarem sua pele. O armário cede com um estalo. (-2 HP)"
            "\n\nLá dentro, uma silhueta feita de raízes se desintegra em cinzas ao seu toque.\n"
            "Não resta nada aqui além de memórias em decomposição.")

WATCHER_UPSTAIRS = GameScene(
    id="watcher_upstairs",
    title="O Quarto do Observador",
    description=("O ar aqui é parado e carregado com o cheiro de remédio vencido.\n"
                "Uma cama de dossel domina o quarto, mas os lençóis foram substituídos por um emaranhado de raízes que formam um ninho central.\n"
                "O assoalho range de forma irregular, como se algo estivesse se movendo sob as tábuas.\n"
                "Não há janelas; apenas molduras vazias pregadas na parede, emoldurando a escuridão absoluta.\n"),
    type=SceneType.MOLDY,
    spore_index=5,
    options=[
        SceneOption("Rasgar as cortinas de raízes sobre a cama de dossel", action=cut_pillow, only_once=True, target_scene_id="watcher_upstairs"),
        SceneOption("Forçar a gaveta inchada da mesa de cabeceira", action=see_bedside_table, only_once=True, target_scene_id="watcher_upstairs"),
        SceneOption("Investigar o armário de roupas trancado por gavinhas", action=investigate_closet, only_once=True, target_scene_id="watcher_upstairs"),
        SceneOption("Voltar para a Sala de Estar", target_scene_id="watcher_living_room")
    ]
)