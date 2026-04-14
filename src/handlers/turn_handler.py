import random

from src.models.entities.player import Player
from src.models.entities.enemy import Enemy

class TurnHandler:
    @staticmethod
    def get_turn_announcement(entity) -> str:
        PLAYER_HEALTHY = [
            f"O destino aguarda seu próximo movimento entre as sombras.",
            f"Sua chama vacila, mas sua vontade é firme.",
            f"O chão de cinzas range sob suas botas.",
            f"Você foca o olhar no inimigo. A vantagem é sua.."
        ]

        PLAYER_CRITICAL = [
            f"{entity.name} está cambaleando, mas firma o passo para o próximo movimento!",
            f"O gosto de ferro e sangue enche sua boca..",
            f"Suas forças se esvaem, mas você não cai sem lutar!",
            f"A escuridão parece mais próxima agora...",
            f"A dor é um aviso, não o fim.."
        ]

        ENEMY_MESSAGES = [
            f"{entity.name} se projeta para frente, buscando o seu medo!",
            f"O ar sibila enquanto {entity.name} prepara um golpe visceral!",
            f"Os olhos de {entity.name} brilham com uma fome necrótica em sua direção.",
            f"{entity.name} se move de forma errática, encurtando a distância!",
            f"Uma aura de podridão emana de {entity.name}. O ataque é iminente!"
        ]

        FALLBACK_MESSAGES = [
            "O ar gela... algo está prestes a acontecer.",
            "A névoa se adensa por um momento, ocultando intenções.",
            "O silêncio da caverna é interrompido por um estalo sinistro.",
            "Um calafrio sobe por sua espinha sem explicação."
        ]

        # --- LÓGICA DE SELEÇÃO POR INSTÂNCIA ---

        # 1. Turno do Jogador
        if isinstance(entity, Player):
            if entity.hp < (entity.max_hp * 0.3):
                return random.choice(PLAYER_CRITICAL)
            return random.choice(PLAYER_HEALTHY)

        # 2. Turno do Inimigo
        elif isinstance(entity, Enemy):
            # Se for o Boss, podemos até injetar uma mensagem exclusiva aqui futuramente
            return random.choice(ENEMY_MESSAGES)

        # 3. Fallback
        else:
            return random.choice(FALLBACK_MESSAGES)