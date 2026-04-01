from src.models.entities.player import Player
from src.models.entities.enemy import Enemy

class TurnHandler:
    @staticmethod
    def get_turn_announcement(entity) -> str:
        # 1. Turno do Jogador
        if isinstance(entity, Player):
            if entity.hp < (entity.max_hp * 0.3): # Se tiver com menos de 30% de vida
                return f"⚠️ {entity.name} está cambaleando, mas firma o passo para o próximo movimento!"
            return f"⚔️ É a sua vez, {entity.name}. O que o brilho da sua luz revela?"

        # 2. Turno do Inimigo
        if isinstance(entity, Enemy):
            return f"👹 {entity.name} se projeta para frente, buscando o seu medo!"

        # 3. Fallback (NPCs ou eventos)
        return "🌀 O ar gela... algo está prestes a acontecer."