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
            print(f"Deseja acender a {lantern.name}?")
            print("\n[1] Sim \n[2] Não")
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
    print("\nVocê aproxima a luz das paredes. Não é ilusão: os rostos na casca cinzenta\n"
        "têm dentes de madeira e olhos feitos de nós de árvore. Eles parecem ter sido\n"
        "absorvidos vivos. Uma inscrição feita com unhas arrancadas na madeira diz:\n"
        "'O frio seca a alma antes de virar lenha'. Sua sanidade oscila.\n")
    print(feedback)
    return

def seek_necrotic_hole(player):
    # Risco e Recompensa: Pode achar óleo, mas pode levar dano de farpa
    print("\nVocê enfia a mão em uma fenda entre troncos que parecem costelas secas.")
    time.sleep(1)

    if random.random() < 0.15:
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
    print("[1] Sim \n[2] Não")
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
        GameState.set("defeat_sentinel", True)
        return (
            f"\nA criatura desmorona em farpas e cinzas. Você recupera o item: {ambar.name}\n"
            "📖 Dica: Este âmbar obtido permite enxergar através de névoas de musgo e revela coisas antes impossíveis de serem vistas."
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
        SceneOption("Seguir o caminho da paredes de madeira morta e veias fluorescentes de seiva negra.", requirement=lambda p: GameState.get("focus_active"), target_scene_id="abism_second_chamber"),
        SceneOption("Vasculhar fendas em busca de suprimentos", action=seek_necrotic_hole, only_once=True, target_scene_id="abism_first_chamber"),
        SceneOption("Observar os rostos fundidos nas paredes", action=see_faces_wall, only_once=True, target_scene_id="abism_first_chamber"),
        SceneOption("Investigar o vulto sob a raiz central", only_once=True, action=investigate_figure,target_scene_id="abism_first_chamber"),
        SceneOption("Recuar para a entrada da caverna", target_scene_id="dense_florest")
    ]
)

# SEGUNDA CÂMARA

def second_chamber_description(player):
    if not GameState.get("focus_active"):
        return (
        "O teto do Átrio das Artérias curva-se baixo sobre sua cabeça, forçando-o a uma postura de submissão.\n"
        "As paredes aqui não são de pedra fria, mas de uma biomassa que pulsa com um calor febril e doentio.\n"
        "O som é o que mais castiga: um tamborilar rítmico, abafado e orgânico, como o coração de um gigante\n"
        "enterrado vivo sob toneladas de terra negra. Três bulbos imensos, do tamanho de tórax humanos, brilham\n"
        "com uma luz violácea e translúcida, bloqueando a única passagem visível com uma rede de tendões vivos."
        )
    return ("Através do brilho alaranjado do âmbar, a realidade biológica se torna transparente. Você vê que as\n"
            "raízes não cresceram sozinhas: elas seguem conduítes de cobre e canos de ferro que serpenteiam por\n"
            "trás da carne vegetal. Fantasmas estáticos de luz azulada revelam silhuetas de homens em jalecos brancos\n"
            "que outrora operaram válvulas agora fundidas ao limo. Onde antes havia apenas escuridão, agora você\n"
            "enxerga um duto de ventilação metálico escondido atrás do bulbo superior, exalando um ar gélido e estéril."
            )

def read_research_notes(player):
    GameState.set("read_hospital_hint", True)
    return ("\nVocê encontra uma prancheta de metal presa por fibras musculares à parede.\n"
            "O papel está amarelado, mas a escrita é técnica e fria:\n"
            "> 'Paciente 732 reagiu violentamente à infusão de Seiva Negra.'\n"
            "> 'O crescimento tecidual superou a estrutura óssea. O hospital precisa de mais sedativos.'\n"
            "> 'Se o Limo chegar ao porão, não haverá como selar a passagem.'")

def scavenge_artery_piles(player):
    print("\nVocê vasculha uma pilha de sedimentos e ossos que o Limo não conseguiu digerir.\n")
    cura = ItemDB.get_item("unguento_fibroso")
    oleo = ItemDB.get_item("oleo_carne")
    print(f"🔎 Entre dentes e terra, você resgata: {cura.name} e {oleo.name}.")
    InventoryHandler.add_item(player, cura)
    InventoryHandler.add_item(player, oleo)
    return


def find_hidden_medical_kit(player):
    print("\nO brilho alaranjado do Âmbar atravessa a parede de músculos e foca em um brilho frio.")
    item_medico = ItemDB.get_item("unguento_fibroso")
    InventoryHandler.add_item(player, item_medico)
    # Bônus de Sanidade por encontrar "esperança"
    player.sanity = min(player.max_sanity, player.sanity + 15)
    return f"✨ Você resgatou um {item_medico.name}. Sentir o metal frio da civilização acalma seus nervos. [+15 Sanidade]"


def reveal_pulse_weakness(player):
    # O Âmbar mostra exatamente qual bulbo está sobrecarregado
    print("\nSob a lente do Âmbar, os três bulbos revelam suas cores reais.")
    print("O bulbo do Teto brilha em um vermelho pulsante, indicando ser o núcleo de energia.")

    # Mecânica útil: O próximo combate ou puzzle fica 50% mais fácil
    GameState.set("pulse_hint_revealed", True)
    return "👁️ Você agora entende o fluxo. O próximo desafio de sincronia não oferecerá resistência."

ABISM_SECOND_CHAMBER = GameScene(
    id="abism_second_chamber",
    title="O Átrio das Artérias",
    description=second_chamber_description,
    type="cave",
    options=[
        SceneOption("Ler a prancheta de metal encravada na raiz", action=read_research_notes, only_once=True, target_scene_id="abism_second_chamber"),
        SceneOption("Vasculhar as pilhas de detritos orgânicos", action=scavenge_artery_piles, only_once=True, target_scene_id="abism_second_chamber"),
        SceneOption(
            "Segredo: Ler as inscrições fluorescentes na raiz do Teto",
            requirement=lambda p: GameState.get("focus_active"),
            action=lambda p: "A inscrição diz: 'O primeiro pulsar vem do céu...'",
            only_once=True,
            target_scene_id="abism_second_chamber"
        ),
        SceneOption(
            "Segredo: Extrair suprimentos do compartimento metálico oculto",
            requirement=lambda p: GameState.get("focus_active"),
            action=find_hidden_medical_kit,
            only_once=True,
            target_scene_id="abism_second_chamber"
        ),
        SceneOption("Segredo: Tentar sincronizar os batimentos dos Bulbos", action=reveal_pulse_weakness, only_once=True, requirement=lambda p: GameState.get("focus_active"), target_scene_id="abism_second_chamber"),
        SceneOption("Continuar sincronizando os batimentos para abrir caminho", requirement= lambda p: GameState.get("pulse_hint_revealed"), target_scene_id="start_artery_puzzle"),
        SceneOption("Voltar para a câmara anterior", target_scene_id="abism_first_chamber")
    ]
)

# PUZZLE DA SEGUNDA CÂMARA

def puzzle_description(player):
    if not GameState.get("focus_active"):
        return ("Você se posiciona diante da parede de carne. O calor é opressor e o som das 'batidas' faz seus dentes vibrarem.\n"
        "Para abrir caminho, você precisa tocar os três bulbos na ordem em que a vida flui pelo Abismo.\n"
        "Toque o bulbo errado, e a dissonância atingirá seu sistema nervoso como um chicote elétrico.\n")
    return ("\nVocê se posiciona diante da parede de carne. O calor é opressor e o som das 'batidas' faz seus dentes vibrarem.\n"
        "Para abrir caminho, você precisa tocar os três bulbos na ordem em que a vida flui pelo Abismo.\n"
        "Toque o bulbo errado, e a dissonância atingirá seu sistema nervoso como um chicote elétrico.\n"
        "\nAtravés da lente alaranjada, você vê trilhas de luz negra conectando os bulbos.\n"
        "A energia brota do TETO, desce para a ESQUERDA e morre na DIREITA.\n"
        "Siga o fluxo para não ser consumido.\n")

def interact_bulb(player, bulb_number):
    """
    Lógica de interação individual com cada bulbo.
    Sequência Correta: Teto (3) -> Esquerda (1) -> Direita (2)
    """
    if GameState.get("abism_puzzle_solved"):
        return "\nO bulbo está inerte e vazio agora."
    correct_sequence = [3, 1, 2]  # Teto, Esquerda, Direita
    current_step = GameState.get("puzzle_step", 0)

    print(f"\nVocê estende a mão e toca a membrana quente do Bulbo {bulb_number}...")
    time.sleep(1.5)

    if bulb_number == correct_sequence[current_step]:
        # ACERTOU O PASSO
        GameState.set("puzzle_step", current_step + 1)

        if GameState.get("puzzle_step") == 3:
            GameState.set("abism_puzzle_solved", True)
            return (
                "\n✨ HARMONIA ALCANÇADA!\n"
                "Ao tocar o último nó, um som agudo de cristal se partindo ecoa pela câmara.\n"
                "A parede de músculos central se contrai violentamente, desabando em uma pilha de\n"
                "matéria orgânica flácida. O cheiro de decomposição é forte, mas o caminho para\n"
                "a Terceira Câmara está finalmente aberto."
            )

        return "🎶 O bulbo emite um zumbido baixo e satisfatório. A vibração na sala parece se acalmar levemente."

    else:
        # ERROU A SEQUÊNCIA
        GameState.set("puzzle_step", 0)  # Reseta o progresso

        # Punição severa
        dano_hp = random.randint(1, 3)
        dano_sanidade = 10
        player.hp -= dano_hp
        SanityService.reduce_sanity(player, dano_sanidade)

        return (
            f"\n⚠️ DISSONÂNCIA!\n"
            f"Ao tocar o bulbo fora de sincronia, uma descarga de seiva fervente explode contra sua mão.\n"
            f"O grito da caverna ressoa dentro da sua própria cabeça, bagunçando seus pensamentos.\n"
            f"Você é lançado para trás. O ciclo foi resetado. [-{dano_hp} HP / -{dano_sanidade} Sanidade]"
        )

ABISM_SECOND_CHAMBER_PUZZLE = GameScene(
    id="start_artery_puzzle",
    title="O Plexo Pulsante",
    description=puzzle_description,
    type="cave",
    options=[
        SceneOption("Descer para a Terceira Câmara", requirement=lambda p: GameState.get("abism_puzzle_solved"), target_scene_id="abism_third_chamber"),
        SceneOption("Tocar o Bulbo da Esquerda (Pulsar Rápido)", requirement=lambda p: not GameState.get("abism_puzzle_solved"), action=lambda p: interact_bulb(p, 1), target_scene_id="start_artery_puzzle"),
        SceneOption("Tocar o Bulbo da Direita (Pulsar Lento)", requirement=lambda p: not GameState.get("abism_puzzle_solved"), action=lambda p: interact_bulb(p, 2), target_scene_id="start_artery_puzzle"),
        SceneOption("Tocar o Bulbo do Teto (Pulsar Errático)", requirement=lambda p: not GameState.get("abism_puzzle_solved"), action=lambda p: interact_bulb(p, 3), target_scene_id="start_artery_puzzle"),
        SceneOption("Voltar para o cômodo anterior", target_scene_id="abism_second_chamber")
    ]
)

# TERCEIRA CAMARA

def toggle_amber_vision(player):
    if InventoryHandler.has_item_by_id(player, "cicatriz_ambar"):
        ambar = ItemDB.get_item("cicatriz_ambar")
        feedback = InventoryService.use(player, ambar)
        return feedback
    return None


def read_creepy_photos(player):
    # Sanity hit por ver algo perturbador
    SanityService.reduce_sanity(player, 8)

    # Marcamos que o jogador agora conhece o rosto de alguém importante
    GameState.set("saw_patient_732_photo", True)

    msg = (
        "\nVocê remove uma camada de limo que parece couro velho de cima de uma pilha de cartões.\n"
        "São fotografias em preto e branco, impressas em papel de brometo de prata, "
        "com as bordas roídas por uma umidade ácida.\n"
        "\n--- 🎞️ ARQUIVO DE OBSERVAÇÃO ---\n"
    )

    # Foto 1: Horror Clínico
    msg += (
        "\n1. Uma foto de um paciente amarrado a uma cadeira de metal galvanizado. "
        "Seus olhos estão cobertos por gazes pesadas, mas o que choca é o 'Limo' que "
        "escorre por baixo das bandagens como se fossem lágrimas negras. No verso: 'Paciente 732 - Reação à Fase 2'.\n"
    )

    # Foto 2: O Diretor (Estilo Sanctum)
    msg += (
        "\n2. Uma foto de grupo da equipe médica em frente ao Sanatório. Todos sorriem, "
        "exceto o homem no centro. O rosto dele foi meticulosamente raspado com uma lâmina, "
        "deixando apenas um buraco branco no papel onde deveria estar sua face. Ele segura "
        "uma bengala com um pomo em forma de raiz.\n"
    )

    # Foto 3: O Próprio Nexo
    msg += (
        "\n3. Esta foto é recente. Ela mostra a escada de madeira onde você está agora. "
        "No topo da escada, um vulto humanoide observa a câmera. O vulto não tem pele, "
        "apenas músculos expostos e musgo crescendo onde deveria ser o cabelo. "
        "A legenda diz: 'Ele voltou para casa'."
    )

    msg += "\n\n⚠️ O peso daquelas imagens penetra em sua mente. [-8 Sanidade]"

    return msg

ABISM_THIRD_CHAMBER = GameScene(
    id="abism_third_chamber",
    title="O Nexo do Observador",
    description=("O silêncio aqui é pesado, interrompido apenas pelo zumbido elétrico de cabos que não deveriam estar vivos.\n"
                "O limo, denso e preto como piche, devorou a rocha, revelando a fundação de tijolos cinzentos de uma estrutura humana.\n"
                "Vigas de madeira apodrecida sustentam o teto, cobertas por uma penugem de musgo branco que lembra mofo de necrotério.\n"
                "\nO ar tem o gosto metálico de sangue seco e o cheiro doce e enjoativo de formaldeído.\n"
                "À luz da sua chama, você percebe que os cabos e nervos que você seguia convergem\n"
                "para uma escada de madeira carcomida que sobe em direção a um alçapão.\n"
                "O chão está coalhado de fotos em preto e branco meio digeridas pelo limo,\n"
                "exibindo rostos de pacientes com olhos vendados e sorrisos costurados — fragmentos de memórias que escaparam do Sanatório.\n"),
    type="cave",
    options=[
        SceneOption("Focar sua consciência ao brilho da Cicatriz de Âmba", action=toggle_amber_vision, target_scene_id="abism_third_chamber"),
        SceneOption("Segredo: Descascar a crosta de limo sobre os retratos esquecidos",
                            requirement=lambda p: GameState.get("focus_active"),
                            action=read_creepy_photos,
                            target_scene_id="abism_third_chamber"),
        SceneOption("Escalar as raizes podres em direção ao Porão", target_scene_id="watcher_basement"),
        SceneOption("Retornar ao latejar constante do Átrio das Artérias", target_scene_id="abism_second_chamber")
    ]
)