from src.engine.game_state import GameState
from src.handlers.inventory_handler import InventoryHandler
from src.models.database.item_db import ItemDB
from src.models.entities.scene import GameScene, SceneOption

def description(player):
    if GameState.get("scarecrow_dead") and not InventoryHandler.has_item_by_id(player,"lamparina_musgosa"):
        return (
            "A entrada do casebre agora está escancarada e silenciosa.\n"
            "Onde antes havia uma aura de ameaça, resta apenas o som do vento\n"
            "batendo na porta de madeira podre. A floresta parece ter recuado.\n"
        )
    elif InventoryHandler.has_item_by_id(player,"lamparina_musgosa"):
        return (
        "O campo, antes apenas silencioso, agora parece pulsar em um ritmo doente.\n"
        "A carcaça do espantalho no chão é apenas um monte de palha e sangue negro, mas você\n"
        "sente como se mil olhos estivessem brotando ao seu redor.\n\n"
        "As sombras das árvores se esticam como dedos esqueléticos que tentam agarrar seus pés,\n"
        "e o ar pesa tanto que cada respiração parece queimar seus pulmões. Sua sanidade oscila:\n"
        "os limites entre o que é real e o que é delírio começam a se dissolver no breu.\n\n"
        "Lá adiante, no caminho enlamaçado onde você acordou pela primeira vez, algo grande se move.\n"
        "Não é um movimento natural. É algo rapido, feroz, que deixa um rastro por onde passa\n"
        )
    return ("O matagal termina em um descampado de grama alta e seca, que range sob suas botas.\n"
        "A casa à frente é uma carcaça cinzenta de tábuas descascadas e janelas foscas.\n"
        "Não há sons de pássaros ou insetos; apenas o estalo rítmico de uma tábua solta no deck.\n"
        "A madeira parece ter bebido toda a cor do lugar, restando apenas um mofo pálido.\n"
        "Pela fresta da cortina rasgada, uma luz amarelada pulsa lá dentro... algo está à espreita.\n")

MISTERIOUS_FIELD = GameScene(
    id="misterious_field",
    title="O Campo Misterioso",
    description=description,
    options=[
        SceneOption("Voltar para o Casebre em busca de algo que deixou para trás", requirement=lambda p: GameState.get("scarecrow_dead") and not InventoryHandler.has_item_by_id(p, "chave_porao"), target_scene_id="old_hut"),
        SceneOption("Forçar a porta principal e ver o que está lá dentro", target_scene_id="old_hut",only_once=True),
        SceneOption("Seguir pela trilha que leva até os fundos da casa", target_scene_id="old_hut_backyard",
                    requirement=lambda i: not (InventoryHandler.has_item_by_id(i, "adaga_enferrujada") or InventoryHandler.has_item_by_id(i, "lamparina_musgosa")),
                    only_once=False),
        SceneOption("Recuar para a segurança relativa da trilha enlamaçada", target_scene_id="dense_florest")
    ]
)

MISTERIOUS_FIELD_AFTER_HATCH = GameScene(
    id="misterious_field_after_hatch",
    title="O Campo Agora Estranhamente Silencioso",
    description=description,
    options=[
        SceneOption("Recuar para a segurança relativa da trilha enlamaçada", target_scene_id="dense_florest_attack")
    ]
)