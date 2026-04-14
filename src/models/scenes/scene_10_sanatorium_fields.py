import time
from src.engine.game_state import GameState
from src.engine.scene_bridge import SceneBridge
from src.handlers.inventory_handler import InventoryHandler
from src.models.database.item_db import ItemDB
from src.models.entities.enemy import Enemy
from src.models.entities.scene import GameScene, SceneOption
from src.services.combat_service import CombatService
from src.services.spore_service import SporeService

def mini_boss_introduction(player):
    print(">> A VOZ NA NÉVOA <<\n")

    SporeService.recover_breathe(player)

    print("Você dá o primeiro passo para o vazio do Grande Campo. O ar gélido e carregado\n"
          "de névoa cinzenta atinge seus pulmões, expulsando a última lembrança do cheiro\n"
          "de carne podre da cozinha. O silêncio é absoluto, quebrado apenas pelo range-range\n"
          "da grama morta sob suas botas. Você se sente exposto, um alvo fácil naquele oceano de cinzas.")
    time.sleep(2)
    print("\nDe repente, a névoa se rasga. O silêncio é despedaçado não por um latido, mas por uma súplica distorcida:\n")
    print("'Por favor... ajude... me ajude! Eu estou... preso...'\n")
    time.sleep(3)
    print("*A SILHUETA EMERGE*\n")
    print("Sua metade esquerda é uma massa pulsante de esporos marrons e raízes negras, idênticas ao desenho do porão\n"
          "Mas sua metade direita ainda é humana. O rosto, fundido ao torso oco, está retorcido em uma agonia insuportável, os olhos arregalados de terror.\n\n"
          "A infecção preta eruptindo de seu crânio se calcificou em um pilar de seiva e raízes negras\n"
          "— um chifre grotesco e longo que se curva para o céu, mais ameaçador e estruturado que a simples haste do desenho.\n")
    time.sleep(3)
    print("A voz muda instantaneamente, sobreposta por um chiado seco e faminto:\n"
          "'Crescer... Mais... Mais corpos. Dominar!'\n\n"
          "As raízes negras se tensionam. A mente colmeia fragmentada percebe sua presença.\n"
          "A batalha pelo campo começou, e você não está apenas lutando pela sua vida, mas contra a vontade de uma mente que quer dominar a sua.\n")
    mini_boss = Enemy("Flagelo das Raízes Negras", level=player.level + 1, hp=20, max_hp=20, base_damage=7, damage_reduction=0.3, xp_reward=12)

    print("Você aproveita os poucos segundos que lhe restam para ver se há algo que possa ser útil...")
    SceneBridge.open_inventory(player)

    CombatService.start_combat(player, mini_boss)

    if player.is_alive:
        GameState.set("mist_mini_boss_defeated", True)
        print("O impacto final estilhaça o chifre de seiva calcificada. O som é como vidro temperado se partindo.\n"
               "O Germinado solta um último suspiro — uma mistura de alívio humano e chiado fúngico —\n"
               "antes de desmoronar em uma pilha de cinzas cinzentas e fibras negras que se dissolvem na névoa.\n\n"
               "Onde a criatura tombou, a grama morta foi queimada por um fluido viscoso e escuro.\n")

        InventoryHandler.add_item(player, ItemDB.get_item("fragmento_calcificado"))

        print("\nO campo agora parece maior. E você, mais observado.\n"
               "No rastro da sua morte, você retira uma seiva das raízes negras.\n")

        InventoryHandler.add_item(player, ItemDB.get_item("fluido_ancestral"))
        input("\n[Pressione Enter para continuar...]")

        return "sanatorium_fields"

def description(player) -> str:
    if GameState.get("mist_mini_boss_defeated"):
        return (
                "A névoa sobre o Grande Campo parece ter estagnado. Sem a presença do Germinado,\n"
                "os esporos flutuam em padrões erráticos, como uma colmeia que perdeu sua rainha.\n\n"
                "A silhueta do Sanatório agora é uma presença inescapável no horizonte norte.\n"
                "O rastro de vapor que o Vigia mencionou brilha fracamente sob a luz gélida,\n"
                "serpenteando entre as raízes negras que cobrem o solo como veias expostas.\n"
            )
    return ""


def action_observe_sanatorium(player):
    GameState.set("first_sanatorium_observations", True)

    if GameState.get("first_sanatorium_observations") and not GameState.get("second_sanatorium_observations"):
        GameState.set("second_sanatorium_observations", True)
        return ("\nO Sanatório é uma massa de concreto que parece drenar a luz ao redor.\n"
                "As janelas superiores são como órbitas vazias vigiando o campo em silêncio.")
    elif GameState.get("second_sanatorium_observations") and not GameState.get("third_sanatorium_observations"):
        GameState.set("third_sanatorium_observations", True)
        return ("\nVocê nota o vapor escapando ritmicamente das chaminés metálicas.\n"
                "O prédio parece respirar. O rastro de vapor no solo é o rastro dessa exalação.")
    elif GameState.get("third_sanatorium_observations") and not GameState.get("last_sanatorium_observations"):
        GameState.set("last_sanatorium_observations", True)
        GameState.set("all_sanatorium_observations", True)
        return ("\nAo fixar o olhar nos portões, sua Cicatriz de Âmbar queima sob a pele.\n"
                "A visão distorce e você percebe um padrão de calor sobre o painel numérico do portão.\n"
                "Agora você sabe: a Cicatriz será sua única guia para decifrar os segredos daquele lugar.")
    else:
        return "\nNão há mais nada para ver alí.."

def action_collect_ash_flower(player):
    item_ref = ItemDB.get_item("flor_cinzas")
    inventory_item = InventoryHandler.get_item_by_id(player, "flor_cinzas")
    current_quantity = inventory_item.quantity if inventory_item else 0
    if current_quantity < 3:
        InventoryHandler.add_item(player, item_ref)
        return (
            "\nVocê vasculha entre as raízes negras e encontra uma Flor de Cinzas.\n"
            "Suas pétalas cinzentas pulsam com um calor tênue que acalma seus sentidos."
        )
    else:
        return "\nNão há mais flores inteiras por aqui. A névoa e a batalha consumiram o resto da flora útil."

def action_examine_roots(player):
    return ("\nAs raízes negras cobrem o solo como veias expostas. Elas pulsam levemente quando você as pisa.\n"
            "Você sente que, no momento em que o Germinado caiu, a rede radicular enviou um sinal\n"
            "vibratório em direção ao Sanatório. Eles sabem que você está aqui.")

def action_listen_mists(player):
    return ("\nO silêncio é cortado por um som metálico distante, vindo do Sanatório.\n"
            "Parece o arrastar de correntes ou o bater de uma porta pesada.\n"
            "Na névoa, sussurros sem boca repetem palavras que você quase consegue entender.")

def action_try_return_home(player):
    print(
        "\nVocê vira as costas para o rastro de vapor e tenta refazer seus passos rumo ao sul,\n"
        "buscando a segurança da Casa do Vigia. Mas a névoa atrás de você mudou.\n"
        "Ela se tornou uma muralha densa e estática, e as raízes negras se ergueram do solo\n"
        "como lanças, selando o caminho de onde você veio.\n\n"
        "Sua Cicatriz de Âmbar pulsa com uma dor aguda, um aviso de que seu destino agora\n"
        "está à frente, no Sanatório. O passado foi devorado pela névoa."
    )
    return "sanatorium_fields"

SANATORIUM_FIELDS = GameScene(
    id="sanatorium_fields",
    title="O Grande Campo da Névoa",
    description=description,
    on_enter=mini_boss_introduction,
    on_enter_repeatable=False,
    options=[
        SceneOption("Seguir o rastro de vapor rumo aos Portões do Sanatório", requirement=lambda p: GameState.get("all_sanatorium_observations"),target_scene_id="sanatorium_gates"),
        SceneOption("Observar a estrutura do Sanatório no horizonte", requirement=lambda p: not GameState.get("all_sanatorium_observations"), action=action_observe_sanatorium, target_scene_id="sanatorium_fields"),
        SceneOption("Vasculhar as raízes em busca de plantas", action=action_collect_ash_flower, target_scene_id="sanatorium_fields"),
        SceneOption("Examinar as raízes negras sob seus pés", only_once=True, action=action_examine_roots, target_scene_id="sanatorium_fields"),
        SceneOption("Tentar ouvir o que a névoa esconde", only_once=True, action=action_listen_mists , target_scene_id="sanatorium_fields"),
        SceneOption("Tentar retornar para a segurança da Casa do Observador", action=action_try_return_home, target_scene_id="sanatorium_fields")
    ]
)