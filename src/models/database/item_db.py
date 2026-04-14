import copy
from typing import Dict, Optional
from src.models.entities.item import Item, LightEquipment
from src.models.enums import ItemCategory, ItemSubcategory, StatusEffect

class ItemDB:
    """Tabela completa de registros de Mossrot Sanatorium."""

    _ITEMS: Dict[str, Item] = {

        # --- UTILITÁRIOS & CHAVES ---
        "pa_velha": Item(
            id="pa_velha",
            name="Pá Velha",
            category=ItemCategory.KEY,
            subcategory=ItemSubcategory.STANDARD,
            status_effect=StatusEffect.NONE,
            is_consumable=False,
            is_equippable=False,
            is_equipped=False,
            stackable=False,
            quantity=1,
            value=0,
            passive_bonus=0,
            description="O metal está frio e descascando em lascas de ferrugem..."
        ),

        "pe_de_cabra": Item(
            id="pe_de_cabra",
            name="Pe de Cabra Ensanguentada",
            category=ItemCategory.KEY,
            subcategory=ItemSubcategory.STANDARD,
            status_effect=StatusEffect.NONE,
            is_consumable=False,
            is_equippable=False,
            is_equipped=False,
            stackable=False,
            quantity=1,
            value=0,
            passive_bonus=0,
            description="Uma barra de ferro fundido manchada com um sangue escuro e seco."
        ),

        "caixa_fosforos": Item(
            id="caixa_fosforos",
            name="Caixa de Fósforos",
            category=ItemCategory.KEY,
            subcategory=ItemSubcategory.STANDARD,
            status_effect=StatusEffect.NONE,
            is_consumable=False,
            is_equippable=False,
            is_equipped=False,
            stackable=False,
            quantity=1,
            value=0,
            passive_bonus=0,
            description="Uma pequena caixa úmida, mas cujos palitos permanecem secos."
        ),

        "lamparina_musgosa": LightEquipment(
            id="lamparina_musgosa",
            name="Lamparina de Vidro Musgoso",
            category=ItemCategory.LIGHT,
            subcategory=ItemSubcategory.STANDARD,
            status_effect=StatusEffect.NONE,
            is_consumable=False,
            is_equippable=False,
            is_equipped=False,
            stackable=False,
            quantity=1,
            value=5,
            fuel=100.0,
            max_fuel=100.0,
            fuel_consume=15.0,
            is_lit=False,
            passive_bonus=0,
            description="O vidro está tingido por um lodo esverdeado..."
        ),

        # --- COMBATE (ARMAS / ARMADURAS / PASSIVOS) ---
        "adaga_enferrujada": Item(
            id="adaga_enferrujada",
            name="Adaga Enferrujada",
            category=ItemCategory.WEAPON,
            subcategory=ItemSubcategory.STANDARD,
            status_effect=StatusEffect.BLEEDING,
            is_consumable=False,
            is_equippable=True,
            is_equipped=False,
            stackable=False,
            quantity=1,
            value=2,
            passive_bonus=1,
            description="Uma lâmina curta coberta por ferrugem antiga."
        ),

        "estilete_raiz": Item(
            id="estilete_raiz",
            name="Estilete de Raiz Negra",
            category=ItemCategory.WEAPON,
            subcategory=ItemSubcategory.STANDARD,
            status_effect=StatusEffect.POISONED,
            is_consumable=False,
            is_equippable=True,
            is_equipped=False,
            stackable=False,
            quantity=1,
            value=6,
            passive_bonus=2,
            description="Uma haste longa e retorcida que drena o solo infectado."
        ),

        "colete_couro": Item(
            id="colete_couro",
            name="Colete de Couro Enraizado",
            category=ItemCategory.ARMOR,
            subcategory=ItemSubcategory.STANDARD,
            status_effect=StatusEffect.NONE,
            is_consumable=False,
            is_equippable=True,
            is_equipped=False,
            stackable=False,
            quantity=1,
            value=0.4,
            passive_bonus=0,
            description="A proteção exige um preço orgânico."
        ),

        "fragmento_calcificado": Item(
            id="fragmento_calcificado",
            name="Fragmento Calcificado",
            category=ItemCategory.WEAPON,
            subcategory=ItemSubcategory.STANDARD,
            status_effect=StatusEffect.NONE,
            is_consumable=False,
            is_equippable=False,
            is_equipped=False,
            stackable=False,
            quantity=1,
            value=0,
            passive_bonus=2,
            description="Um pedaço endurecido de seiva negra e osso."
        ),

        # --- COMBUSTÍVEL ---
        "oleo_carne": Item(
            id="oleo_carne",
            name="Óleo de Carne Velha",
            category=ItemCategory.FUEL,
            subcategory=ItemSubcategory.STANDARD,
            status_effect=StatusEffect.NONE,
            is_consumable=True,
            is_equippable=False,
            is_equipped=False,
            stackable=True,
            quantity=1,
            value=30,
            passive_bonus=0,
            description="Líquido rançoso extraído de tecidos podres."
        ),

        "lata_querosene": Item(
            id="lata_querosene",
            name="Lata de Querosene",
            category=ItemCategory.FUEL,
            subcategory=ItemSubcategory.STANDARD,
            status_effect=StatusEffect.NONE,
            is_consumable=True,
            is_equippable=False,
            is_equipped=False,
            stackable=True,
            quantity=1,
            value=50,
            passive_bonus=0,
            description="O frio preservou o óleo, mas o cheiro de morte permanece."
        ),

        # --- CURA (VIDA E SANIDADE) ---
        "tonico_amargo": Item(
            id="tonico_amargo",
            name="Tônico de Seiva Amarga",
            category=ItemCategory.HEAL,
            subcategory=ItemSubcategory.STANDARD,
            status_effect=StatusEffect.NONE,
            is_consumable=True,
            is_equippable=False,
            is_equipped=False,
            stackable=True,
            quantity=1,
            value=5,
            passive_bonus=0,
            description="Um frasco de vidro opaco contendo um líquido viscoso..."
        ),

        "flor_cinzas": Item(
            id="flor_cinzas",
            name="Flor de Cinzas",
            category=ItemCategory.HEAL,
            subcategory=ItemSubcategory.HYBRID,
            status_effect=StatusEffect.NONE,
            is_consumable=True,
            is_equippable=False,
            is_equipped=False,
            stackable=True,
            quantity=1,
            value=10,
            passive_bonus=0,
            description="Suas fibras derretem na língua, trazendo um breve alívio."
        ),

        "unguento_fibroso": Item(
            id="unguento_fibroso",
            name="Unguento de Fibras Vivas",
            category=ItemCategory.HEAL,
            subcategory=ItemSubcategory.STANDARD,
            status_effect=StatusEffect.NONE,
            is_consumable=True,
            is_equippable=False,
            is_equipped=False,
            stackable=True,
            quantity=1,
            value=10,
            passive_bonus=0,
            description="Uma pasta avermelhada que parece pulsar levemente..."
        ),

        "tonico_opio": Item(
            id="tonico_opio",
            name="Tônico de Ópio do Sanatório",
            category=ItemCategory.SANITY,
            subcategory=ItemSubcategory.STANDARD,
            status_effect=StatusEffect.NONE,
            is_consumable=True,
            is_equippable=False,
            is_equipped=False,
            stackable=True,
            quantity=1,
            value=15,
            passive_bonus=0,
            description="Promete um silêncio artificial para mentes estilhaçadas."
        ),

        "fluido_ancestral": Item(
            id="fluido_ancestral",
            name="Extrato de Coração da Seiva Maldita",
            category=ItemCategory.HEAL,
            subcategory=ItemSubcategory.STANDARD,
            status_effect=StatusEffect.NONE,
            is_consumable=True,
            is_equippable=False,
            is_equipped=False,
            stackable=True,
            quantity=1,
            value=25,
            passive_bonus=0,
            description="O frasco está quente ao toque..."
        ),

        "sais_clinicos": Item(
            id="sais_clinicos",
            name="Sais de Suporte Clínico",
            category=ItemCategory.HEAL,
            subcategory=ItemSubcategory.HYBRID,
            status_effect=StatusEffect.NONE,
            is_consumable=True,
            is_equippable=False,
            is_equipped=False,
            stackable=True,
            quantity=1,
            value=15,
            passive_bonus=0,
            description="Um pequeno frasco de vidro verde com uma tampa de cortiça."
        ),

        # --- PROGRESSÃO & LORE ---
        "chave_sanatorio": Item(
            id="chave_sanatorio",
            name="Chave das Galerias de Vapor",
            category=ItemCategory.KEY,
            subcategory=ItemSubcategory.STANDARD,
            status_effect=StatusEffect.NONE,
            is_consumable=False,
            is_equippable=False,
            is_equipped=False,
            stackable=False,
            quantity=1,
            value=0,
            passive_bonus=0,
            description="Esta chave abre o caminho para o centro da semente."
        ),

        "chave_porao": Item(
            id="chave_porao",
            name="Chave de Falange",
            category=ItemCategory.KEY,
            subcategory=ItemSubcategory.STANDARD,
            status_effect=StatusEffect.NONE,
            is_consumable=False,
            is_equippable=False,
            is_equipped=False,
            stackable=False,
            quantity=1,
            value=0,
            passive_bonus=0,
            description="Uma peça grotesca onde a madeira se fundiu a um osso..."
        ),

        "chave_vapor": Item(
            id="chave_vapor",
            name="Chave de Latão: Setor 02",
            category=ItemCategory.KEY,
            subcategory=ItemSubcategory.STANDARD,
            status_effect=StatusEffect.NONE,
            is_consumable=False,
            is_equippable=False,
            is_equipped=False,
            stackable=False,
            quantity=1,
            value=0,
            passive_bonus=0,
            description="Uma chave industrial robusta e morna ao toque."
        ),

        "cicatriz_ambar": Item(
            id="cicatriz_ambar",
            name="Cicatriz de Âmbar",
            category=ItemCategory.VIEW,
            subcategory=ItemSubcategory.UNIQUE,
            status_effect=StatusEffect.FOCUSED,
            is_consumable=False,
            is_equippable=True,
            is_equipped=False,
            stackable=False,
            quantity=1,
            value=0,
            passive_bonus=0,
            description="Revela as veias de seiva negra que pulsam nas paredes."
        ),

        "anel_latao": Item(
            id="anel_latao",
            name="Anel de Latão Oxidado",
            category=ItemCategory.LORE,
            subcategory=ItemSubcategory.STANDARD,
            status_effect=StatusEffect.NONE,
            is_consumable=False,
            is_equippable=False,
            is_equipped=False,
            stackable=False,
            quantity=1,
            value=0,
            passive_bonus=0,
            description="Um círculo simples de latão gravado com '732'."
        )
    }

    @staticmethod
    def get_item(item_id: str) -> Optional[Item]:
        template = ItemDB._ITEMS.get(item_id)
        if template:
            return copy.deepcopy(template)
        return None