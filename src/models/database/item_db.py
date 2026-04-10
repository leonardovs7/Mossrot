import copy
from typing import Dict, Optional
from src.models.entities.item import Item, LightEquipment

class ItemDB:
    """Tabela macabra de registros de itens do jogo."""

    _ITEMS: Dict[str, Item] = {

        # --- UTILITÁRIOS ---
        "pa_velha": Item(
            id="pa_velha",
            name="Pá Velha",
            description="O metal está frio e descascando em lascas de ferrugem...",
            category="util",
            subcategory="dig",
            is_consumable=False,
            is_equippable=False,
            is_equipped=False,
            stackable=False,
            quantity=1,
            value=0,
            passive_bonus=0
        ),

        "pe_de_cabra": Item(
            id="pe_de_cabra",
            name="Pe de Cabra Ensanguentada",
            description="Uma barra de ferro fundido, pesada e fria ao toque manchada com um sangue escuro e seco",
            category="util",
            subcategory="break",
            is_consumable=False,
            is_equippable=False,
            is_equipped=False,
            stackable=False,
            quantity=1,
            value=0,
            passive_bonus=0
        ),

        "lamparina_musgosa": LightEquipment(
            id="lamparina_musgosa",
            name="Lamparina de Vidro Musgoso",
            description="O vidro está tingido por um lodo esverdeado...",
            category="light",
            subcategory="light",
            is_consumable=False,
            is_equippable=False,
            is_equipped=False,
            stackable=False,
            quantity=1,
            value=5,
            fuel=100.0,
            max_fuel=100.0,
            fuel_consume=10.0,
            is_lit=False,
            passive_bonus=0
        ),

        # --- COMBATE ---

        #armas
        "adaga_enferrujada": Item(
            id="adaga_enferrujada",
            name="Adaga Enferrujada",
            description="Uma lâmina curta coberta por ferrugem antiga.",
            category="weapon",
            subcategory="dagger",
            is_consumable=False,
            is_equippable=True,
            is_equipped=False,
            stackable=False,
            quantity=1,
            value=2,
            passive_bonus=0
        ),

        "estilete_raiz": Item(
            id="estilete_raiz",
            name="Estilete de Raiz Negra",
            description="Uma haste longa e retorcida extraída das profundezas do sistema radicular que drena o solo infectado sob estas fundações.",
            category="weapon",
            subcategory="poison",
            is_consumable=False,
            is_equippable=True,
            is_equipped=False,
            stackable=False,
            quantity=1,
            value=6,
            passive_bonus=2
        ),

        #armadura
        "colete_couro": Item(
            id="colete_couro",
            name="Colete de Couro Enraizado",
            description="O couro te esconde, mas a raiz te sustenta. É um lembrete constante de que, neste lugar, a proteção exige um preço orgânico.",
            category="armor",
            subcategory="plate",
            is_consumable=False,
            is_equippable=True,
            is_equipped=False,
            stackable=False,
            quantity=1,
            value=0.4,
            passive_bonus=0
        ),

        #itens de combate ativos (precisam ser usados)
        "fragmento_calcificado": Item(
            id="fragmento_calcificado",
            name="Fragmento Calcificado",
            description="Um pedaço endurecido de seiva negra e osso, extraído do crânio do Germinado.",
            category="combat",
            subcategory="passive",
            is_consumable=False,
            is_equippable=False,
            is_equipped=False,
            stackable=False,
            quantity=1,
            value=0,
            passive_bonus=2
        ),

        #COMBUSTIVEL

        "caixa_fosforos": Item(
            id="caixa_fosforos",
            name="Caixa de Fósforos",
            description="Uma pequena caixa úmida, mas cujos palitos permanecem secos.",
            category="util",
            subcategory="util",
            is_consumable=False,
            is_equippable=False,
            is_equipped=False,
            stackable=False,
            quantity=1,
            value=0,
            passive_bonus=0
        ),

        "oleo_carne": Item(
            id="oleo_carne",
            name="Óleo de Carne Velha",
            description="Líquido rançoso extraído de tecidos podres. Queima com fumaça preta.",
            category="fuel",
            subcategory="fuel",
            is_consumable=True,
            is_equippable=False,
            is_equipped=False,
            stackable=True,
            quantity=1,
            value=30,
            passive_bonus=0
        ),

        "lata_querosene": Item(
            id="lata_querosene",
            name="Lata de Querosene",
            description="O frio preservou o óleo, mas o cheiro de morte que escapou da geladeira vai ficar nas suas roupas por muito tempo.",
            category="fuel",
            subcategory="fuel",
            is_consumable=True,
            is_equippable=False,
            is_equipped=False,
            stackable=True,
            quantity=1,
            value=50,
            passive_bonus=0
        ),

        # --- CURA ---
        "tonico_amargo": Item(
            id="tonico_amargo",
            name="Tônico de Seiva Amarga",
            description="Um frasco de vidro opaco contendo um líquido viscoso...",
            category="heal",
            subcategory="weakHeal",
            is_consumable=True,
            is_equippable=False,
            is_equipped=False,
            stackable=True,
            quantity=1,
            value=5,
            passive_bonus=0
        ),

        "flor_cinzas": Item(
            id="flor_cinzas",
            name="Flor de Cinzas",
            description="Uma planta de pétalas cinzentas que cresce perto do vapor. Suas fibras derretem na língua, trazendo um breve alívio ao corpo e aos sentidos..",
            category="heal",
            subcategory="multiHeal",
            is_consumable=True,
            is_equippable=False,
            is_equipped=False,
            stackable=True,
            quantity=1,
            value=10,
            passive_bonus=0
        ),

        "unguento_fibroso": Item(
            id="unguento_fibroso",
            name="Unguento de Fibras Vivas",
            description="Uma pasta avermelhada que parece pulsar levemente...",
            category="heal",
            subcategory="mediumHeal",
            is_consumable=True,
            is_equippable=False,
            is_equipped=False,
            stackable=True,
            quantity=1,
            value=10,
            passive_bonus=0
        ),

        "tonico_opio": Item(
            id="tonico_opio",
            name="Tônico de Ópio do Sanatório",
            description=(
                "Um frasco de vidro âmbar com o timbre do Sanatório de Vidro Fosco gravado no vidro. "
                "Contém um extrato denso e escuro de papoula misturado a sedativos químicos. "
                "O aroma adocicado e enjoativo promete um silêncio artificial para mentes "
                "estilhaçadas, abafando os sussurros que vêm das paredes de limo."
            ),
            category="heal",
            subcategory="sanityHeal",
            stackable=True,
            is_consumable=True,
            is_equippable=False,
            is_equipped=False,
            quantity=1,
            value=15,
            passive_bonus=0
        ),

        "fluido_ancestral": Item(
            id="fluido_ancestral",
            name="Extrato de Coração da Seiva Maldita",
            description="O frasco está quente ao toque...",
            category="heal",
            subcategory="strongHeal",
            is_consumable=True,
            is_equippable=False,
            is_equipped=False,
            stackable=True,
            quantity=1,
            value=25,
            passive_bonus=0
        ),

        "sais_clinicos": Item(
            id="sais_clinicos",
            name="Sais de Suporte Clínico",
            description=("Um pequeno frasco de vidro verde com uma tampa de cortiça."),
            category="heal",
            subcategory="multiHeal",
            is_consumable=True,
            is_equippable=False,
            is_equipped=False,
            stackable=True,
            quantity=1,
            value=15,
            passive_bonus=0
        ),

        # --- LORE E CHAVES ---

        "chave_sanatorio": Item(
            id="chave_sanatorio",
            name="Chave das Galerias de Vapor",
            description="Esta chave não abre apenas uma porta; ela abre o caminho para o centro da semente..",
            category="util",
            subcategory="key",
            is_consumable=False,
            is_equippable=False,
            is_equipped=False,
            stackable=False,
            quantity=1,
            value=0,
            passive_bonus=0
        ),

        "chave_porao": Item(
            id="chave_porao",
            name="Chave de Falange",
            description="Uma peça grotesca onde a madeira se fundiu a um osso...",
            category="util",
            subcategory="key",
            is_consumable=False,
            is_equippable=False,
            is_equipped=False,
            stackable=False,
            quantity=1,
            value=0,
            passive_bonus=0
        ),

        "cicatriz_ambar": Item(
            id="cicatriz_ambar",
            name="Cicatriz de Âmbar",
            description="Revela as veias de seiva negra que pulsam nas árvores mortas.",
            category="view",
            subcategory="view",
            is_consumable=False,
            is_equippable=True,
            is_equipped=False,
            stackable=False,
            quantity=1,
            value=0,
            passive_bonus=0
        ),

        "anel_latao": Item(
            id="anel_latao",
            name="Anel de Latão Oxidado",
            description="Um círculo simples e pesado de latão. Na parte interna, há uma gravação feita às pressas, quase ilegível, onde se lê: '732 - Propriedade do Estado'.",
            category="lore",
            subcategory="lore",
            is_consumable=False,
            is_equippable=False,
            is_equipped=False,
            stackable=False,
            quantity=1,
            value=0,
            passive_bonus=0
        )

    }

    @staticmethod
    def get_item(item_id: str) -> Optional[Item]:
        """Busca e clona um item do banco."""
        template = ItemDB._ITEMS.get(item_id)
        if template:
            return copy.deepcopy(template)
        return None