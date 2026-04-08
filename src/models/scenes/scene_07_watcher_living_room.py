from src.engine.game_state import GameState
from src.handlers.inventory_handler import InventoryHandler
from src.models.database.item_db import ItemDB
from src.models.entities.scene import GameScene, SceneOption
from src.services.sanity_service import SanityService


def seek_bookshelf(player):
    if GameState.get("focus_active"):
        if not InventoryHandler.has_item_by_id(player, "estilete_raiz"):
            print("\nSeus dedos deslizam pela madeira porosa, sentindo o relevo das letras douradas que\n"
                  "o tempo quase apagou. Enquanto a maioria dos livros parece colada pelo mofo,\n"
                  "sua percepção aguçada nota uma dissonância: o volume 'O Ciclo das Raízes' não\n"
                  "possui um grão de poeira sequer.\n"
                  "\nAo puxá-lo, o mecanismo range com um som de ossos quebrados e a estante desliza,\n"
                  "revelando um cofre de ferro fundido embutido na parede fria. No centro da porta,\n"
                  "um teclado numérico mecânico com teclas gastas espera por uma sequência...\n"
                  "o rastro de sangue seco nas teclas sugere que alguém tentou abri-lo com pressa.\n")
            print("O visor de vidro baço do cofre brilha fracamente. Digite o código de acesso (3 dígitos):")
            code = input("> ")
            if code == "732":
                print("\nO mecanismo solta um suspiro de ar viciado. A porta se abre pesadamente,\n"
                      "revelando um estojo de madeira apodrecida forrado com musgo seco.\n"
                      "Dentro, repousa uma arma que parece ter sido mais cultivada do que forjada.\n")
                InventoryHandler.add_item(player, ItemDB.get_item("estilete_raiz"))
                return
            else:
                SanityService.reduce_sanity(player, 1)
                return "O cofre permanece selado. O erro ecoa no vazio..."
        return "\nVocê já encontrou tudo o que era necessário ali.."
    return ("\nSeus dedos deslizam pela madeira porosa, sentindo o relevo das letras douradas que o tempo quase apagou.\n"
            "Entre os volumes de botânica fúngica, um livro parece não pertencer ao caos...")

def seek_couch(player):
    print("O sofá exala um cheiro pungente de mofo e algo orgânico em decomposição. O veludo vermelho, agora quase preto pela sujeira, está rasgado em padrões que lembram garras.\n")
    if not InventoryHandler.has_item_by_id(player, "colete_couro"):
        print("Seus dedos tocam algo áspero e resistente sob as molas quebradas. Você puxa com força e revela uma peça de vestuário feita de couro grosso,\n"
              "marcada com símbolos que você marcadas nas paredes do porão do observador..\n")
        InventoryHandler.add_item(player, ItemDB.get_item("colete_couro"))
        return "O couro ainda parece levemente quente, como se tivesse sido usado recentemente, mas não há ninguém na sala."
    return "Você procura qualquer outra coisa que possa te ajudar futuramente, mas não encontra nada útil.."

def see_photos(player):
    if GameState.get("focus_active"):
        return ("Ao estreitar os olhos e ignorar as rachaduras do vidro, você percebe algo que a luz fraca da sala tentava ocultar.\n"
                "No canto inferior da fotografia, onde o rosto do patriarca foi arrancado, há uma marcação frenética.\n"
                "\nEscavado na polpa do papel e preenchido com um marrom seco que você reconhece como sangue velho, está o número: 732.\n"
                "O traço é trêmulo, como se quem o escreveu estivesse perdendo a consciência... ou a sanidade.")
    else:
        return ("O vidro estilhaçado reflete seu rosto de forma distorcida.\n"
                "Atrás da imagem riscada da família que um dia habitou este lugar, um pedaço de papel amarelado clama por atenção.")

WATCHER_LIVING_ROOM = GameScene(
    id="watcher_living_room",
    title="Sala de Estar do Observador",
    description=("O que um dia foi um ambiente de conforto, agora é um mausoléu de lembranças apodrecidas.\n"
                "O papel de parede floral está descolando como pele morta,\n"
                "revelando manchas de mofo negro que parecem pulsar em um ritmo lento.\n"
                "\nUm sofá de veludo rasgado ocupa o centro, voltado para uma televisão de tubo cujo vidro está estilhaçado\n"
                "de dentro para fora. O cheiro de poeira e esporos é tão denso que você consegue\n"
                "sentir o gosto metálico no fundo da garganta. O silêncio aqui não é vazio; é expectante.\n"),
    type="moldy",
    spore_index=15,
    options=[
        SceneOption("Dedilhar as lombadas da estante de carvalho em decomposição", action=seek_bookshelf, target_scene_id="watcher_living_room"),
        SceneOption("Explorar a superfície rasgada do sofá de veludo", action=seek_couch, target_scene_id="watcher_living_room"),
        SceneOption("Verificar o vidro quebrado do porta-retrato sobre a lareira", action=see_photos, target_scene_id="watcher_living_room"),
        SceneOption("Desafiar a garganta escura da escadaria que leva ao andar de cima", action=lambda p: print("Cada degrau emite um gemido de protesto sob suas botas, como se a madeira estivesse viva e sentindo o seu peso.\n"
                                                                                                         "A escuridão lá em cima não é apenas a ausência de luz; é uma massa densa que parece vibrar com o latejar das raízes\n"
                                                                                                         "que descem pelas paredes, estrangulando o corrimão."), target_scene_id="watcher_upstairs"),
        SceneOption("Perseguir a mancha de mofo que pulsa na parede norte", action=lambda p: print("O mofo parece desenhar o contorno de uma porta que não deveria estar ali. Ao se aproximar, os esporos brilham fracamente."), target_scene_id="watcher_kitchen"),
        SceneOption("Descer ao porão para recuperar um pouco do folêgo", target_scene_id="watcher_basement")

    ]
)