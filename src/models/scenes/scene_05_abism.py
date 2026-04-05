import random
import time

from src.engine.game_state import GameState
from src.handlers.inventory_handler import InventoryHandler
from src.models.database.item_db import ItemDB
from src.models.entities.enemy import Enemy
from src.models.entities.scene import GameScene, SceneOption
from src.services.combat_service import CombatService
from src.services.inventory_service import InventoryService
from src.services.sanity_service import SanityService


def no_entrance(player):
    print("\nVocê tenta dar um passo, mas a escuridão é um muro sólido.\n"
          "O frio do Limo rasteja pelas suas pernas e o pânico aperta o peito.\n"
          "Sem luz, avançar é suicídio. Seus instintos gritam para você\n"
          "dar meia volta enquanto ainda consegue sentir o rastro do ar puro que vem da entrada.")
    input("\n[Pressione Enter para voltar...]")
    if GameState.get("putrid_dog_dead"):
        return "dense_florest_attack"
    return "dense_florest"

def verify_lamp(player):
    if InventoryHandler.has_item_by_id(player, "lamparina_musgosa"):
        lantern = ItemDB.get_item("lamparina_musgosa")
        if not lantern.is_lit:
            print("\n[1] Sim | [2] Não")
            choice = input("> ")
            if choice == "1":
                feedback = InventoryService.use(player, lantern)
                print(feedback)
                print("Aquela fraca, porém intensa, luz revela que o musgo nas paredes não está\n"
              "apenas crescendo — ele está digerindo a pedra. Sob o brilho,\n"
              "as sombras se retorcem freneticamente, como vermes fugindo.\n\n"
              "O caminho à frente está visível, mas a cada passo a escuridão\n"
              "parece mais densa, tentando sufocar a sua pequena chama.")
                return "abism_first_chamber"
            else:
               return no_entrance(player)
    else:
        return no_entrance(player)

LIME_ABISM = GameScene(
    id="lime_abism",
    title="Abismo de Limo",
    description=("O ar aqui dentro é estagnado, com um gosto metálico de terra\n"
      "velha e algo doce, como carne apodrecendo sob o sol.\n"
      "O musgo rasteja pelas paredes em padrões que lembram veias\n"
      "pulsantes, tomando formas grotescas que parecem te observar.\n\n"
      "A umidade é um abraço frio que abafa seus sentidos. No Abismo,\n"
      "o silêncio só é quebrado pelo gotejar rítmico vindo do breu."),
    on_enter=verify_lamp,
    on_enter_repeatable=True
)

# PRIMEIRA CÂMARA

def see_faces_wall(player):
    sanityReducing = random.randint(1, 5)
    feedback = SanityService.reduce_sanity(player, sanityReducing)
    print(feedback)
    return (
        "\nVocê aproxima a luz das paredes. Não é ilusão: os rostos na casca cinzenta\n"
        "têm dentes de madeira e olhos feitos de nós de árvore. Eles parecem ter sido\n"
        "absorvidos vivos. Uma inscrição feita com unhas arrancadas na madeira diz:\n"
        "'O frio seca a alma antes de virar lenha'. Sua sanidade oscila."
    )

def seek_necrotic_hole(player):
    # Risco e Recompensa: Pode achar óleo, mas pode levar dano de farpa
    print("\nVocê enfia a mão em uma fenda entre troncos que parecem costelas secas.")
    time.sleep(1)

    if random.random() < 0.3:
        player.hp -= 3
        return "⚠️ Uma farpa de madeira necrótica perfura sua palma. Dói como fogo. [-3 HP]"

    if not InventoryHandler.has_item_by_id(player, "oleo_carne"):
        InventoryHandler.add_item(player, ItemDB.get_item("oleo_carne"))
        return "🔎 Você encontra um frasco de piche vegetal. Serve como combustível bruto."

    return "🔎 A fenda está vazia, restando apenas serragem e pó cinzento."

def investigate_figure(player):
    # O clímax que construímos
    print("\n sob a raiz em forma de forca parece o epicentro do frio.")
    print("O silêncio aqui é absoluto, quebrado apenas pelo estalo da sua própria pele ressecando.")
    print("\nDeseja realmente tocar no vulto para investigar?")
    print("[1] Sim | [2] Não")
    choice = input("> ")

    if choice != "1":
        return "\nVocê recua. O medo de se tornar parte dessa lenha é maior que a curiosidade."

    print("\nVocê estende a mão. O 'corpo' é uma escultura oca de galhos e casca seca.")
    print("No peito aberto do cadáver, um estilhaço de âmbar pulsa como um coração de brasa.")
    time.sleep(2)

    print("\n*CRACK*! O som de osso e madeira se partindo explode na sala.")
    print("O Cerne de Cadáver se levanta. Galhos afiados rasgam o que restava de pele,")
    print("e uma seiva negra jorra como sangue fervente das juntas da criatura.")
    time.sleep(2)

    enemy = Enemy(name="Cerne de Cadáver", level=3, hp=10, max_hp=10, damage_reduction=0.3, base_damage=4, xp_reward=8)
    CombatService.start_combat(player, enemy, is_surprise=False)

    if player.is_alive:
        ambar = ItemDB.get_item("cicatriz_ambar")
        InventoryHandler.add_item(player, ambar)
        InventoryService.use(player, ambar)
        GameState.set("defeat_sentinel", True)
        return (
            "\nA criatura desmorona em farpas e cinzas. Você recupera o item:\n"
            "📖 Dica: Este âmbar obtido permite enxergar através de névoas de musgo."
        )
    return ""

ABISM_FIRST_CHAMBER = GameScene(
    id="abism_first_chamber",
    title="O Átrio das Cascas",
    description=("Um salão vasto e sufocante, onde o teto desaparece em um emaranhado de\n"
        "raízes negras. As paredes de madeira morta exibem rostos humanos fundidos\n"
        "à casca cinzenta. O chão é coberto por uma camada espessa de cinzas e\n"
        "serragem que abafa seus passos. No centro, sob uma raiz que desce como\n"
        "uma forca, um vulto permanece imóvel, guardando algo que brilha.\n"),
    type="cave",
    options=[
        SceneOption("Entrar na sala encoberta por musgos brilhantes", requirement=lambda p: GameState.get("defeat_sentinel"), target_scene_id="abism_second_chamber"),
        SceneOption("Observar os rostos fundidos nas paredes", action=see_faces_wall, target_scene_id="abism_first_chamber"),
        SceneOption("Vasculhar fendas em busca de suprimentos", action=seek_necrotic_hole, only_once=True, target_scene_id="abism_first_chamber"),
        SceneOption("Investigar o vulto sob a raiz central", action=investigate_figure,target_scene_id="abism_first_chamber"),
        SceneOption("Recuar para a entrada da caverna", target_scene_id="dense_florest")
    ]
)