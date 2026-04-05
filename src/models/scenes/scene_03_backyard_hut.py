from src.engine.game_state import GameState
from src.handlers.inventory_handler import InventoryHandler
from src.models.database.item_db import ItemDB
from src.models.entities.item import Item
from src.models.entities.scene import SceneOption, GameScene


def description(player):
    if GameState.get("hatch_open"):
        return (
               "O montante de terra foi removido. A escotilha de ferro está exposta,\n"
               "revelando uma fechadura moldada em osso que parece esperar pela sua chave.\n"
               "Um frio húmido sobe pelas frestas do metal.\n"
               )
    return (
            "Atrás da casa, o mato é alto e sufocante. Sob uma camada espessa de musgo,\n"
            "você nota uma elevação estranha no solo, perfeitamente retangular.\n"
            "O ar aqui parece mais pesado, como se a terra estivesse a prender o fôlego.\n"
           )

def handle_dig(player):
    if InventoryHandler.has_item_by_id(player, "pa_velha"):
        GameState.set("hatch_digged", True)
        return ("\nO metal da pá corta o musgo e a terra com um som de carne a ser rasgada."
                "Após alguns minutos de esforço, revelas uma escotilha de ferro pesada."
                "No centro, há uma entrada para chave que parece feita de material orgânico.")
    return None

BACKYARD_HUT = GameScene(
    id="old_hut_backyard",
    title="Fundos do Casebre",
    description=description,
    options=[
        SceneOption(
            text="Remover a terra com a pá, tentando não fazer muito barulho..",
            target_scene_id="old_hut_backyard",
            requirement=lambda i: not GameState.get("hatch_digged"),
            action=handle_dig
        ),
        SceneOption(
            text="Inserir a Chave de Falange na fechadura e torcer para que abra..",
            target_scene_id="hatch",
            requirement=lambda i: InventoryHandler.has_item_by_id(i, "pa_velha") and GameState.get("hatch_digged") and not GameState.get("hatch_open"),
            action= lambda p: ("\nVocê encaixa a Chave de Falange na fechadura de osso e ela entra de forma justa, quase orgânica...\n"
            "Ao girar, um estalo duro e metálico ecoa pelo quintal silencioso — um som pesado de engrenagens que não sentem o óleo há décadas.\n"
            "A escotilha cede com um rangido arrastado, revelando um vão negro que exala o cheiro de terra e segredos guardados.")
        ),
        SceneOption(text="Entrar no Porão Abandonado", target_scene_id="hatch",
                    requirement=lambda p: GameState.get("hatch_open") and not (
                                InventoryHandler.has_item_by_id(p, "adaga_enferrujada") and InventoryHandler.has_item_by_id(p,"lamparina_musgosa"))),
            SceneOption("Voltar para a frente da casa, longe desse lugar", target_scene_id="misterious_field",
                        requirement=lambda p: not (
                                    InventoryHandler.has_item_by_id(p,"adaga_enferrujada") and InventoryHandler.has_item_by_id(p,"lamparina_musgosa"))),
            SceneOption("Voltar para a frente da casa.. não tem mais nada para ver aqui",
                        target_scene_id="misterious_field_after_hatch",
                            requirement=lambda p: (InventoryHandler.has_item_by_id(p,"adaga_enferrujada") and InventoryHandler.has_item_by_id(p,"lamparina_musgosa")))
    ]
)