import time

from src.engine.game_state import GameState
from src.handlers.inventory_handler import InventoryHandler
from src.models.database.item_db import ItemDB
from src.models.entities.scene import GameScene, SceneOption
from src.services.inventory_service import InventoryService


def enter_basement(player):
    GameState.set("hatch_open", True)
    if GameState.get("hatch_open") and InventoryHandler.has_item_by_id(player, "chave_porao"):
        InventoryHandler.remove_item(player, "chave_porao")
    return (
        "O ar frio do porão sobe para encontrar seu rosto, carregando um cheiro metálico\n"
        "de sangue seco misturado ao bofo de papel velho. Os degraus rangem sob seu peso como se a madeira estivesse prestes a ceder.\n\n"
        "Ao puxar a cordinha, a lâmpada solta um estalo elétrico e começa a emitir um\n"
        "zumbido baixo e irritante, como se estivesse sob esforço constante.\n"
        "A luz amarelada não alcança os cantos, onde sombras densas parecem se esconder da sua presença.\n"
        "\nNo centro, o chão de concreto está manchado por poças de um líquido escuro e viscoso.\n"
        "À esquerda, uma mesa de carvalho jaz coberta por uma poeira tão espessa que parece uma pele acinzentada.\n"
        "À direita, o armário maciço parece uma sentinela mofada, com fungos brancos que lembram teias de aranha descendo pelas laterais.\n"
    )

def going_table(player):
    if not InventoryHandler.has_item_by_id(player,"adaga_enferrujada"):
        dagger =  ItemDB.get_item("adaga_enferrujada")
        InventoryHandler.add_item(player, dagger)
        print("\nDeseja equipar o item agora?"
              "\n[1] Sim \n[2] Não")
        choice = input("> ")
        if choice == "1":
            feedback = InventoryService.use(player, dagger)
            print(feedback)
        return (
                "\nAs travas da maleta cedem com um estalo seco. Dentro dela, repousando sobre\n"
                "documentos oficiais agora ilegíveis, você encontra uma adaga de lâmina curta.\n"
                "A crosta de ferrugem que a cobre é tão densa e irregular que parece ter se\n"
                "alimentado do tempo e de algo mais... algo que deixou o metal doente.\n\n"
                "O cabo de madeira está tomado por um mofo cinzento e aveludado que parece\n"
                "soltar esporos ao seu toque. Ao empunhá-la, um calafrio percorre sua espinha;\n"
                "mesmo velha, a lâmina transmite um peso hostil, como se estivesse faminta."
                )
    return None

def going_back(player):
    if not InventoryHandler.has_item_by_id(player,"lamparina_musgosa"):
        return ("\nAo colocar o pé no primeiro degrau para subir, um peso estranho se instala no seu peito.\n"
                "Você sente que está esquecendo algo vital naquele breu, algo que pode ser a diferença entre a vida e a morte quando a luz do dia sumir.\n"
                "Antes de fechar a escotilha, você lança um último olhar para trás:\n"
                "a sensação de que olhos invisíveis estão cravados na sua nuca, observando cada movimento seu de dentro das sombras do armário, é tão real que você quase consegue ouvir uma respiração pesada vindo do escuro.")

    return ("Com o metal frio e musgoso da lamparina agora em mãos, o ar do porão parece subitamente mais leve, mas de um jeito perturbador.\n"
            "Aquela vigilância opressiva que parecia emanar de cada canto escuro se dissipou, como se a 'coisa' que residia ali tivesse decidido que este cômodo não é mais interessante.\n"
            "Enquanto você sobe, fica a dúvida amarga: a presença sumiu, ou ela apenas se moveu para outro lugar, esperando por você lá fora?")

def collect_lantern(player):
    lantern = ItemDB.get_item("lamparina_musgosa")
    InventoryHandler.add_item(player, lantern)
    GameState.set("lamparina_coletada", True)
    return (
        "\nSeus dedos se fecham ao redor da alça de ferro gelada, que parece pegajosa\n"
        "devido ao musgo que a recobre. Ao levantá-la do caixote, você sente um calor\n"
        "irregular emanando do vidro — não é o calor seco do fogo, mas algo úmido,\n"
        "como se o objeto estivesse vivo.\n\n"
        "Lá dentro, a substância viscosa borbulha e estala com um som que lembra\n"
        "gordura animal sendo frita. A luz pálida que ela emite é instável e projeta\n"
        "sombras que parecem se esticar e se desprender das paredes conforme você se move.\n"
        "Você agora tem um pouco mais de clareza nesse breu, mas as formas que a luz\n"
        "revela nos cantos do porão fazem você desejar ter ficado no escuro."
    )


def collect_matches(player):
    if not InventoryHandler.has_item_by_id(player,"caixa_fosforos"):
        fosforos = ItemDB.get_item("caixa_fosforos")
        InventoryHandler.add_item(player, fosforos)
        return (
            "\nVocê puxa o puxador de ferro, mas a madeira nem sequer range. Está\n"
            "trancado por dentro. Um som abafado de algo raspando na parte interna\n"
            "da madeira faz você soltar a maçaneta instantaneamente, sentindo um\n"
            "gelo percorrer seus dedos. Melhor não insistir...\n\n"
            "Ao se afastar do armário, seu olhar recai sobre uma pequena mesinha\n"
            "de cabeceira ao lado. Sobre o tampo manchado, repousa uma caixa de\n"
            "fósforos gasta. O som seco dos palitos ao chacoalhá-la é o primeiro\n"
            "sinal de esperança nesse lugar. Você a guarda no bolso imediatamente."
        )
    return (
        "\nO armário permanece trancado e a mesinha agora está vazia. O silêncio\n"
        "daquele canto do quarto é pesado demais para ser ignorado."
    )

HATCH = GameScene(
    id="hatch",
    title="O Porão Abandonado",
    description=enter_basement,
    options=[
        SceneOption(
            text="Aproximar-se da mesa velha e examinar as fotos e a maleta",
            target_scene_id="hatch",
            action=going_table,
            only_once=True
        ),
        SceneOption(
            text="Tentar forçar a porta do grande armário mofado à direita",
            target_scene_id="hatch",
            action=collect_matches,
            only_once=True
        ),
        SceneOption(
            text="Pegar a lamparina musgosa sobre o caixote",
            target_scene_id="hatch",
            requirement=lambda i: not (InventoryHandler.has_item_by_id(i, "lamparina_musgosa")),
            action=collect_lantern,
            only_once=True
        ),
        SceneOption(
            text="Limpar a poeira de um pequeno espelho rachado na parede",
            target_scene_id="hatch",
            action=lambda p: (
                "\nVocê passa a mão pelo vidro turvo. Por um breve segundo, seu reflexo\n"
                "parece demorar um milissegundo a mais para se mover. O vidro está\n"
                "gelado como gelo, apesar do calor da lâmpada acima."
            ),
            only_once=True
        ),
        SceneOption(
            text="Inspecionar um ralo de ferro entupido no centro do chão",
            target_scene_id="hatch",
            action=lambda p: (
                "\nUm líquido escuro e viscoso borbulha lentamente lá dentro.\n"
                "O cheiro que emana dali lembra carne esquecida ao sol.\n"
                "Há fios de cabelo presos na grade de metal... longos demais para serem humanos."
            ),
            only_once=True
        ),
        SceneOption("Subir a escada e voltar para o quintal", action=going_back ,target_scene_id="misterious_field_after_hatch")
    ]
)