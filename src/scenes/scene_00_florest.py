import random

from src.engine.game_state import GameState
from src.handlers.inventory_handler import InventoryHandler
from src.models.database.item_db import ItemDB
from src.models.entities.enemy import Enemy
from src.models.entities.scene import GameScene, SceneOption
from src.services.combat_service import CombatService
from src.services.sanity_service import SanityService

def description(player):
    validador: bool = GameState.get("entrou_caverna")
    if not validador:
        return (
        "Você está sozinho sobre a terra úmida de uma floresta densa.\n"
        "As sombras das árvores balançam como garras negras ao vento.\n"
        "Você olha para as próprias mãos e nota uma pequena lasca de madeira brotando da sua carne..\n"
        "Os arbustos próximos tremem levemente... como se algo estivesse à espreita.\n"
        )
    return (
        "O ar da floresta agora parece estagnado, como se as árvores estivessem prendendo o fôlego.\n"
        "A abertura da caverna às suas costas sopra um hálito frio e úmido que faz a lasca em sua mão\n"
        "latejar em um ritmo doentio. Você escapou da escuridão profunda, mas o silêncio aqui fora\n"
        "é tão pesado quanto o breu lá de dentro. Algo mudou... ou talvez você é que não seja mais o mesmo.\n"
    )

def dogs_description(player):
    if player.sanity == 100:
        SanityService.reduce_sanity(player, random.randint(3,15))
        input("\n[Pressione Enter para continuar...]")
        return (
        "Você volta ao lugar onde tudo começou, mas o cenário é irreconhecível.\n"
        "A lama onde você acordou agora parece um pântano de piche negro, borbulhando\n"
        "com um odor de carniça que tranca a garganta. No centro do caminho, duas\n"
        "figuras grotescas bloqueiam a passagem.\n\n"
        "São cães, ou o que restou deles. Seus corpos são uma amálgama perturbadora:\n"
        "galhos retorcidos servem como costelas, musgo rasteja por feridas abertas e\n"
        "pedaços de carne pendem de 'ossos' feitos de madeira velha. Eles não latem.\n"
        "O único som que emite é o estalo de madeira seca e o chiado de moscas.\n"
        )
    return (
        "Você volta ao lugar onde tudo começou, mas o cenário é irreconhecível.\n"
        "A lama onde você acordou agora parece um pântano de piche negro, borbulhando\n"
        "com um odor de carniça que tranca a garganta. No centro do caminho, duas\n"
        "figuras grotescas bloqueiam a passagem.\n\n"
        "São cães, ou o que restou deles. Seus corpos são uma amálgama perturbadora:\n"
        "galhos retorcidos servem como costelas, musgo rasteja por feridas abertas e\n"
        "pedaços de carne pendem de 'ossos' feitos de madeira velha. Eles não latem.\n"
        "O único som que emite é o estalo de madeira seca e o chiado de moscas.\n"
    )

def find_shovel(player):
    if not InventoryHandler.has_item_by_id(player,"pa_velha"):
        shovel = ItemDB.get_item("pa_velha")
        InventoryHandler.add_item(player, shovel)

        return ("\nSuas mãos tremem ao tocar o cabo. A madeira está úmida, como se transpirasse."
                "\nVocê sente que essa ferramenta já foi usada para algo que não deveria ser desenterrado.")

    return "\nVocê mexe nos arbustos secos, mas só encontra terra preta e folhas mortas."

def combat_putrid_dogs(player):
    dog1 = Enemy(name="Casca", level=1, hp=3, maxHp=3, defenseReduction=0.5, baseDamage=2, xpReward=2)
    dog2 = Enemy(name="Medula", level=1, hp=4, maxHp=4, defenseReduction=0.0, baseDamage=1, xpReward=3)
    enemies = [dog1, dog2]
    CombatService.start_combat(player, enemies, isSurprise=True)

def seek_dogs_loot(player):
    cura = ItemDB.get_item("tonico_amargo")
    InventoryHandler.add_item(player, cura)
    return ("\nVocê revira a massa de carne podre e galhos secos. No que parece ser\n"
            "o estômago de uma das feras, você encontra um frasco de líquido límpido.")

DENSE_FLOREST = GameScene(
    id="dense_florest",
    title="A Floresta Densa",
    description=description,
    options=[
        SceneOption("Se aproximar dos arbustos para analisar?", target_scene_id="dense_florest", action=find_shovel, only_once=True),
        SceneOption("Observar o caminho enlamaçado à frente — marcas estranhas parecem seguir adiante...", target_scene_id="misterious_field"),
        SceneOption("Seguir o rastro que leva até uma abertura escura entre as árvores densas", target_scene_id="lime_abism")
    ]
)

DENSE_FLOREST_ATTACK = GameScene(
    id="dense_florest_attack",
    title="O Ataque na Floresta Densa",
    description=dogs_description,
    on_enter=combat_putrid_dogs,
    options=[
        SceneOption("Vasculhar os restos das abominações", target_scene_id="dense_florest_attack", action=seek_dogs_loot ,only_once=True),
        SceneOption("Seguir o rastro que leva até uma abertura escura entre as árvores densas", target_scene_id="lime_abism")
    ]
)