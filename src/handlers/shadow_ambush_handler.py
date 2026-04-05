import random

from src.models.entities.enemy import Enemy
from src.models.entities.player import Player
from src.services.combat_service import CombatService
from src.services.light_service import LightService
from src.services.loot_service import LootService

class ShadowAmbushHandler:
    @staticmethod
    def trigger_shadow_ambush(player: Player):
        print("\nA escuridão ao seu redor se torna densa e faminta...")
        print("Algo rasteja do breu absoluto, atraído pelo seu medo.\n")

        # Nomes temáticos
        names_list = ['Vulto Apodrecido', 'Forma Corrompida', 'Sombra Enraizada', 'Aparição Podre']
        final_name = random.choice(names_list)

        # Escalonamento básico baseado no nível do jogador
        # Isso garante que a emboscada seja sempre um desafio justo
        level_mult = max(1, player.level)
        hp = random.randint(1, 8) * level_mult
        defense = random.uniform(0.02, 0.06)
        damage = random.randint(1, 4)
        xp_reward = random.randint(1, 3) * level_mult

        enemy = Enemy(
            name=final_name,
            level=player.level,
            hp=hp,
            max_hp=hp,
            damage_reduction=defense,
            base_damage=damage,
            xp_reward=xp_reward
        )

        # Inicia o combate (o parâmetro isSurprise pode dar vantagem ao inimigo)
        CombatService.start_combat(player, enemy, is_surprise=True)

        if player.is_alive:
            print("\nVocê venceu as sombras!")
            # Orquestração de serviços pós-vitória
            feedback_light = LightService.force_relight(player)
            loot_msg = LootService.check_loot(player)

            print(loot_msg)
            print(feedback_light)
        else:
            print("\nA escuridão finalmente o consumiu...")