from enum import Enum, auto

class SceneType(Enum):
    NORMAL = auto()      # Corredores e salas padrão (sem efeitos)
    DARK = auto()        # Escuridão total (exige luz ou causa erro de navegação)
    MOLDY = auto()       # Infestação de mofo (drena vida/sanidade por turno)