from src.engine.game_state import GameState
from src.handlers.inventory_handler import InventoryHandler
from src.models.database.item_db import ItemDB
from src.models.entities.enemy import Enemy
from src.models.entities.scene import GameScene, SceneOption
from src.services.combat_service import CombatService


def handle_combat(player):
    print("\n")
    scarecrow = Enemy(name="Espantalho Vivo", level=1, hp=3, max_hp=3, damage_reduction=0.0, base_damage=1, xp_reward=4)
    CombatService.start_combat(player, scarecrow, is_surprise=True)
    if player.hp > 0:
        GameState.set("scarecrow_dead", True)
        return (
                "\nA carcaça do espantalho desmorona, as costuras de palha cedendo sob seu golpe final.\n"
                "O silêncio que retorna ao casebre é pesado, interrompido apenas pela sua respiração ofegante.\n"
                "O perigo imediato se foi, mas o ar continua carregado de eletricidade estática."
                )
    return None

def collect_key(player):
    key = ItemDB.get_item("chave_porao")
    if not InventoryHandler.has_item_by_id(player, key):
        InventoryHandler.add_item(player, key)
        return ("\nAo puxar a chave, a pele colada ao metal se rasga com um som úmido."
                "\nVocê sente uma pontada de dor na própria mão, como se tivesse ferido a si mesmo.\n"
                "\nO que resta da criatura é apenas um amontoado silencioso de podridão.\n"
                "O ar esfriou e um peso opressor se instala em seus ombros.\n"
                "Você sente que olhos invisíveis o observam das sombras...\n"
                "Seu corpo clama para que você saia deste lugar o mais rápido possível.")
    return "\nO que resta do espantalho é apenas madeira podre e carne seca."

OLD_HUT = GameScene(
    id="old_hut",
    title="O Casebre",
    description=(
        "Você entra. A luz amarelada no canto pulsa como um coração doente.\n"
        "O frio é paralisante. Antes que você possa dar o primeiro passo para trás,\n"
        "a silhueta de musgo e carne podre se desprende da escuridão..."
    ),
    on_enter=handle_combat,
    options=[
        SceneOption("Se aproximar do que restou da criatura e investigar..", target_scene_id="scarecrow_body"),
        SceneOption("Não olhar para trás e sair logo desta casa", target_scene_id="misterious_field")
    ]
)

SCARECROW_BODY = GameScene(
    id="scarecrow_body",
    title="Carcaça Imóvel",
    description=(
        "Você se aproxima com cuidado. O resto da criatura é um emaranhado úmido\n"
        "de palha, musgo e algo que lembra pele curtida.\n"
        "No peito da carcaça, o metal da chave brilha fracamente, fundido aos ossos,\n"
        "como se o corpo tivesse crescido ao redor dela para protegê-la."
    ),
    options=[
        SceneOption(
            text="Tentar desentranhar a Chave de Falange da estrutura daquele monstro..",
            target_scene_id="misterious_field",
            action=collect_key,
            only_once=True
        ),
        SceneOption("Ignorar a chave e sair antes que o ar acabe", target_scene_id="misterious_field") # Volta para a sala principal
    ]
)