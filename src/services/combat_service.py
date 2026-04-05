import time
import sys
import random
from typing import List, Union

from src.handlers.xp_handler import LevelHandler
from src.models.entities.entity import Entity
from src.models.entities.player import Player
from src.models.entities.enemy import Enemy
from src.handlers.combat_handler import CombatHandler


class CombatService:
    @staticmethod
    def execute_turn(attacker: Entity, defender: Entity, skip_menu: bool = False):
        # Resetamos a defesa no início do turno (usando o padrão snake_case)
        attacker.is_defending = False

        if isinstance(attacker, Player) and not skip_menu:
            print(f"\n--- Turno de {attacker.name} ---")
            print(f"❤️ HP: {attacker.hp}/{attacker.max_hp}")
            # Note: Verifique se 'weapon' e 'armor' são objetos ou strings no seu modelo
            print(f"🗡️ Arma: {attacker.weapon} | 🛡️ Armadura: {attacker.armor}\n")
            print("1 - Atacar")
            print("2 - Defender")

            choice = input("Escolha sua ação: \n> ")

            if choice == "2":
                attacker.is_defending = True
                print(f"🛡️ {attacker.name} entrou em postura defensiva!")
                return

                # 1. Gerar dano usando o CombatHandler
        raw_damage = CombatHandler.attack(attacker)

        # 2. Aplicar dano e mitigação usando o CombatHandler
        # O CombatHandler já faz os prints de "recebeu X de dano"
        CombatHandler.defend(defender, raw_damage)

        time.sleep(1)

    @staticmethod
    def start_combat(player: Player, enemies: Union[Enemy, List[Enemy]], is_surprise: bool = False):
        # Garante que enemies seja uma lista
        if not isinstance(enemies, list):
            enemies = [enemies]

        if is_surprise:
            print(f"⚠️ SURPRESA! Você foi emboscado!")
            time.sleep(1)
            for e in enemies:
                if e.is_alive and player.is_alive:
                    CombatService.execute_turn(e, player)

        print(f"\n⚔️ O combate começou! Oponentes: {', '.join([e.name for e in enemies])}")

        # Loop principal de combate
        while player.is_alive and any(e.is_alive for e in enemies):
            alive_enemies = [e for e in enemies if e.is_alive]

            # --- TURNO DO JOGADOR ---
            if len(alive_enemies) > 1:
                print("\nInimigos à frente:")
                for i, e in enumerate(alive_enemies, 1):
                    print(f"{i} - {e.name} (HP: {e.hp}/{e.max_hp})")

                print(f"\n❤️ Seu HP: {player.hp}/{player.max_hp}")
                target_input = input("Alvo ou 'd' para defender: \n> ").lower()

                if target_input == 'd':
                    player.is_defending = True
                    print(f"🛡️ {player.name} foca na defesa!")
                else:
                    try:
                        idx = int(target_input) - 1
                        target = alive_enemies[idx]
                        CombatService.execute_turn(player, target, skip_menu=True)
                    except (ValueError, IndexError):
                        print("Você hesitou e perdeu a oportunidade!")
            else:
                # Se só há um inimigo, o menu interno do execute_turn cuida disso
                CombatService.execute_turn(player, alive_enemies[0])

            # --- PROCESSAR MORTES E RECOMPENSAS ---
            for e in enemies:
                if not e.is_alive and not hasattr(e, "_already_dead_msg"):
                    print(f"\n🏆 {e.name} sucumbiu!")
                    LevelHandler.earn_xp(player, e.xp_reward)
                    e._already_dead_msg = True

            # --- TURNO DOS INIMIGOS ---
            active_enemies = [e for e in enemies if e.is_alive]
            if active_enemies and player.is_alive:
                print(f"\n--- Turno dos Inimigos ---")
                for e in active_enemies:
                    if player.is_alive:
                        CombatService.execute_turn(e, player)
                        time.sleep(0.5)

        # --- FIM DE JOGO ---
        if not player.is_alive:
            print(f"\n💀 {player.name} foi consumido pela escuridão... Fim de jogo.")
            sys.exit()