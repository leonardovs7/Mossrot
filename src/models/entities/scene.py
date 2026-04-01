from dataclasses import dataclass, field
from typing import List, Callable, Optional, Any, Union

@dataclass
class SceneOption:
    text: str  # Descrição da opção que aparece no menu
    target_scene_id: str  # ID da cena para onde o jogador será levado
    action: Optional[Callable[[Any], Any]] = None  # Função executada ao escolher a opção
    requirement: Optional[Callable[[Any], bool]] = None  # Condição para a opção aparecer
    only_once: bool = False  # Se True, a opção some após ser usada
    is_used: bool = False  # Controle interno para o 'only_once'

@dataclass
class GameScene:
    id: str  # ID único da cena
    title: str  # Título que aparece no topo
    # A descrição pode ser uma String OU uma Função que retorna String (dinâmica)
    description: Union[str, Callable[[Any], str]]
    on_enter: Optional[Callable[[Any], Any]] = None  # Evento ao entrar na cena
    on_enter_repeatable: bool = False  # Define se o evento on_enter acontece toda vez
    options: List[SceneOption] = field(default_factory=list)  # Lista de escolhas
    type: str = "regular"  # Ex: "cave" para disparar emboscadas