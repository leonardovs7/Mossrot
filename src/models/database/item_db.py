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
            value=0
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
            value=0
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
            is_lit=False
        ),

        # --- COMBATE ---
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
            value=2
        ),

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
            value=0
        ),

        #CONSUMIVEIS

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
            value=30
        ),

        "tonico_opio": Item(
            id= "tonico_opio",
            name= "Tônico de Ópio do Sanatório",
            description= (
                "Um frasco de vidro âmbar com o timbre do Sanatório de Vidro Fosco gravado no vidro. "
                "Contém um extrato denso e escuro de papoula misturado a sedativos químicos. "
                "O aroma adocicado e enjoativo promete um silêncio artificial para mentes "
                "estilhaçadas, abafando os sussurros que vêm das paredes de limo."
            ),
            category= "heal",
            subcategory="sanityHeal",
            stackable= True,
            is_consumable=True,
            is_equippable=False,
            is_equipped=False,
            quantity= 1,
            value=25
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
            value=5
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
            value=10
        ),

        "fluido_ancestral": Item(
            id="fluido_ancestral",
            name="Extrato de Coração da Árvore Maldita",
            description="O frasco está quente ao toque...",
            category="heal",
            subcategory="strongHeal",
            is_consumable=True,
            is_equippable=False,
            is_equipped=False,
            stackable=True,
            quantity=1,
            value=25
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
            value=15
        ),

        # --- LORE E CHAVES ---
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
            value=0
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
            value=0
        )
    }

    @staticmethod
    def get_item(item_id: str) -> Optional[Item]:
        """Busca e clona um item do banco."""
        template = ItemDB._ITEMS.get(item_id)
        if template:
            return copy.deepcopy(template)
        return None