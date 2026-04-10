import time

from src.engine.game_state import GameState
from src.handlers.inventory_handler import InventoryHandler
from src.models.database.item_db import ItemDB
from src.models.entities.scene import GameScene, SceneOption
from src.services.sanity_service import SanityService

def see_sink(player):
    print("Você ignora o lodo acumulado e tateia o fundo da pia entupida por raízes. Seus dedos encontram algo metálico preso no ralo.\n"
           "Você puxa o objeto de dentro do ralo entupido. O anel sai acompanhado de um tufo de cabelos grisalhos presos às gavinhas,\n"
           "como se a pia estivesse tentando digerir o antigo dono. Ao segurar a joia barata, um calafrio percorre seus braços.\n"
           "Não é um tesouro, é um vestígio. O Anel de Latão agora pesa no seu bolso, uma lembrança constante de que ninguém sai deste lugar por inteiro.\n")
    InventoryHandler.add_item(player, ItemDB.get_item("anel_latao"))
    print("\nUm círculo simples e pesado de latão, cuja cor original foi quase totalmente devorada por uma pátina esverdeada e crostas de mofo.\n"
          "Ao limpar a sujeira com o polegar, você percebe que o aro não é perfeitamente circular;\n"
          "ele está levemente deformado, como se tivesse sofrido uma pressão imensa enquanto ainda estava no dedo de alguém.\n"
          "Na parte interna, há uma gravação feita às pressas, quase ilegível, onde se lê: '732 - Propriedade do Estado'.\n"
          "O metal está frio, mas ao segurá-lo, você sente uma pulsação rítmica vindo do objeto, sincronizada com o latejar das raízes nas paredes.\n")
    return "Alianças servem para unir duas pessoas. Este anel servia apenas para marcar onde terminava o homem e começava o experimento."

def see_refrigerator(player):
    print("O motor da geladeira emite um chiado irregular, como um animal agonizante.\n"
          "Ao abrir a porta, uma névoa gélida escapa, revelando prateleiras tomadas por uma massa pulsante de fungos alvos.\n")
    InventoryHandler.add_item(player, ItemDB.get_item("lata_querosene"))
    return "\nO frio preservou o óleo, mas o cheiro de morte que escapou da geladeira vai ficar nas suas roupas por muito tempo."

def see_drawer(player):
    print("Você se ajoelha sobre o piso engordurado e força a ponta dos dedos sob a tábua de madeira que range.\n"
          "Com um esforço seco, a madeira cede, revelando um nicho cavado diretamente na terra fria.\n"
          "\nLá dentro, enrolado em um pano de hospital manchado, está um diário médico de capa dura, inchado pela umidade.\n"
          "Ao abri-lo, as páginas soltam um cheiro acre de formol e tinta velha.\n"
          "Entre os registros frenéticos de 'crescimento celular anômalo' e 'falha na contenção do Paciente 732', você sente um volume metálico rígido.\n")
    time.sleep(3)
    print("Escondida em um recorte feito nas últimas páginas do diário, repousa uma chave longa e pesada, feita de ferro batido.\n"
          "Diferente das outras chaves da casa, esta possui o emblema de uma serpente enrolada em uma raiz — o selo oficial da instituição."
          "\nAo segurá-la, o peso do metal parece ancorar sua realidade. Você sabe o que essa chave abre. É o fim deste labirinto doméstico e o começo de algo muito maior.\n")
    InventoryHandler.add_item(player, ItemDB.get_item("chave_sanatorio"))
    GameState.set("get_sanctum_key", True)
    return ("\nA chave em suas mãos pulsa levemente. Você recorda dos avisos no porão: "
           "\nnão tente os portões principais. Esta chave pertence aos fundos, "
           "\nàs galerias de vapor da Lavanderia. É por lá que você deve entrar.")

def force_focus_kitchen(player):
    if GameState.get("focus_active"):
        return "\nSua visão já está sintonizada com a dissonância deste lugar. O ar vibra com veias de luz negra."
    GameState.set("focus_active", True)
    print(
        "\nVocê ignora o nojo e fixa o olhar no pulsar rítmico do mofo negro sobre o fogão.\n"
        "O mundo ao redor começa a derreter; as cores desaparecem, restando apenas o brilho doentio\n"
        "das raízes que correm por trás das paredes de pedra. Sua cabeça lateja como se um prego fosse\n"
        "martelado em sua têmpora, mas agora... agora você enxerga o que estava oculto.\n"
    )
    feedback = SanityService.reduce_sanity(player, 10)
    return feedback

WATCHER_KITCHEN = GameScene(
    id="watcher_kitchen",
    title="A Cozinha do Observador",
    description=("O cheiro de carne podre e terra úmida é quase sólido aqui.\n"
                 "teto está coberto por uma massa de mofo negro que goteja um líquido oleoso sobre a mesa central,\n"
                 "como se a casa estivesse chorando óleo.\n"
                 "\nUtensílios de metal, oxidados e retorcidos, pendem de ganchos enferrujados, balançando sem vento algum.\n"
                 "balcão de pedra está rachado, e das frestas brotam pequenas gavinhas que parecem buscar o calor da sua lamparina.\n"),
    type="moldy",
    spore_index=25,
    options=[
        SceneOption("Mergulhar as mãos na gordura fria da pia de metal", action=see_sink, only_once=True, target_scene_id="watcher_kitchen"),
        SceneOption("Abrir a porta da geladeira que exala um frio antinatural", action=see_refrigerator, only_once=True, target_scene_id="watcher_kitchen"),
        SceneOption("Concentrar sua visão no pulsar do limo e tentar enxergar além",
                    action=force_focus_kitchen,
                    requirement=lambda p: not GameState.get("focus_active"),
                    target_scene_id="watcher_kitchen"),
        SceneOption("Remexer as gavetas de utensílios enferrujados", only_once=True, action=lambda p: GameState.set("get_drawer", True) and print("As gavetas resistem, inchadas pela umidade. Ao forçá-las, o som de metal raspando no metal ecoa pela casa.\n"
                                                                                            "Você encontra facas cegas e garfos tortos que parecem ter sido usados para algo que não era comer."),
                                                                                             target_scene_id="watcher_kitchen"),
        SceneOption("Segredo: Remover a tábua solta sob o fogão", action=see_drawer, only_once=True, requirement=lambda p: GameState.get("focus_active") and GameState.get("get_drawer"), target_scene_id="watcher_kitchen"),
        SceneOption("Forçar a porta pesada da cozinha e encarar o que quer que aguarde no horizonte", action=lambda p: print("\nVocê gira a chave e chuta a porta. O ar gélido da noite invade seus pulmões,\n expulsando o cheiro de carne podre da cozinha.\n"), target_scene_id="sanatorium_fields"),
        SceneOption("Voltar para a Sala de Estar", target_scene_id="watcher_living_room")
    ]
)