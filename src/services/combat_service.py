import os
import time
import sys
import random
from typing import List, Union

from src.engine.game_state import GameState
from src.engine.scene_bridge import SceneBridge
from src.handlers.turn_handler import TurnHandler
from src.handlers.xp_handler import LevelHandler
from src.models.entities.entity import Entity
from src.models.entities.player import Player
from src.models.entities.enemy import Enemy
from src.handlers.combat_handler import CombatHandler
from src.models.enums import StatusEffect
from src.services.status_service import StatusService


class CombatService:
    @staticmethod
    def execute_turn(attacker: Entity, defender: Entity, skip_menu: bool = False, is_surprise: bool = False):


        attacker.is_defending = False

        if isinstance(attacker, Player) and not skip_menu:
            print(f"\n=== [TURNO DE {attacker.name}] ===".upper())
            start_turn_announce = TurnHandler.get_turn_announcement(attacker)
            print(f"{start_turn_announce}")
            print(f"❤️ HP: {attacker.hp}/{attacker.max_hp} | 🗡️ {attacker.weapon} (+{attacker.current_weapon_damage}) | 🛡️ {attacker.armor} (+{attacker.current_armor_defense * 100}%)")
            print("\n1 - Atacar | 2 - Defender | i - Inventário")

            choice = input("Escolha sua ação: \n> ")

            if choice == "1":
                pass

            elif choice == "2":
                attacker.is_defending = True
                print(f"🛡️ {attacker.name} entrou em postura defensiva!")
                return

            elif choice == "i":
                SceneBridge.open_inventory(attacker)
                return

            else:
                return CombatService.execute_turn(attacker, defender)

        if isinstance(attacker, Enemy): #se for o inimigo atacando:
            # tem 20% de chance padrão de defender ao invés de atacar / se estiver com a vida abaixo de 30% sobe para 40%
            if not is_surprise: # só defende se o combate não for uma emboscada
                hp_ratio = attacker.hp / attacker.max_hp
                defense_chance = 0.40 if hp_ratio < 0.3 else 0.20
                if random.random() < defense_chance:
                    attacker.is_defending = True
                    print(f"\n>> {attacker.name} recua, protegendo seus pontos vitais e antecipando seu golpe!")
                    time.sleep(1)
                    return

        #processamento do ataque realizado pelo jogador ao selecionar 1 ou no turno do inimigo que não se defende:

        # 1. Gerar dano usando o CombatHandler
        raw_damage = CombatHandler.attack(attacker)

        # 2. Aplicar dano e mitigação usando o CombatHandler
        CombatHandler.defend(attacker, defender, raw_damage)
        time.sleep(1)

        if isinstance(attacker, Player) and defender.is_alive and attacker.equipped_weapon:
            weapon = attacker.equipped_weapon
            # Checa se a arma possui um efeito e se não é NONE
            if hasattr(weapon, 'status_effect') and weapon.status_effect != StatusEffect.NONE:
                if random.random() <= 1:  # 50% de chance de procar o efeito
                    feedback = StatusService.apply_status(defender, weapon.status_effect, weapon)
                    if feedback:
                        print(feedback)
                        time.sleep(1)

        time.sleep(1)

    @staticmethod
    def start_combat(player: Player, enemies: Union[Enemy, List[Enemy]], is_surprise: bool = False):
        os.system('cls' if os.name == 'nt' else 'clear')
        player.in_combat = True
        # Garante que enemies seja uma lista
        if not isinstance(enemies, list):
            enemies = [enemies]

        if is_surprise:
            print(f"⚠️ SURPRESA! Você foi emboscado!")
            time.sleep(1)
            for e in enemies:
                if e.is_alive and player.is_alive:
                    CombatService.execute_turn(e, player, is_surprise=True)

        print(f"\n⚔️ O combate começou! Oponentes: {', '.join([e.name for e in enemies])}")

        # Loop principal de combate
        while player.is_alive and any(e.is_alive for e in enemies):
            alive_enemies = [e for e in enemies if e.is_alive]

            # --- TURNO DO JOGADOR ---
            if isinstance(player, Player):
                print(f"\n=== [TURNO DE {player.name}] ===".upper())
                start_turn_announce = TurnHandler.get_turn_announcement(player)
                print(f"{start_turn_announce}")
                print(f"❤️ HP: {player.hp}/{player.max_hp} | 🗡️ {player.weapon} (+{player.current_weapon_damage}) | 🛡️ {player.armor} (+{player.current_armor_defense * 100}%)")

            choice = input("\n1 - Atacar | 2 - Defender | i - Inventário\nEscolha sua ação: \n> ").lower()

            if choice == "1":
                if len(alive_enemies) > 1:
                    print("\nInimigos à frente:")
                    for i, e in enumerate(alive_enemies, 1):
                        print(f"{i} - {e.name} (HP: {e.hp}/{e.max_hp})")

                    target_input = input("\nEscolha o alvo que deseja atacar: \n> ").lower()
                    try:
                        idx = int(target_input) - 1
                        target = alive_enemies[idx]
                        CombatService.execute_turn(player, target, skip_menu=True)
                    except (ValueError, IndexError):
                        print("Você hesitou e perdeu a oportunidade!")
                else:
                    CombatService.execute_turn(player, alive_enemies[0], skip_menu=True)
            elif choice == "2":
                player.is_defending = True
                print(f"🛡️ {player.name} foca na defesa!")
            elif choice == "i":
                SceneBridge.open_inventory(player)
            else:
                print("\n❌ Comando inválido! A indecisão custou seu tempo de reação.")

            # --- PROCESSAR MORTES E RECOMPENSAS ---
            for e in enemies:
                if not e.is_alive and not hasattr(e, "_already_dead_msg"):
                    print(f"\n🏆 {e.name} sucumbiu!")
                    LevelHandler.earn_xp(player, e.xp_reward)
                    e._already_dead_msg = True

            # --- TURNO DOS INIMIGOS ---
            active_enemies = [e for e in enemies if e.is_alive]
            if active_enemies and player.is_alive:
                if len(active_enemies) == 1:
                    print(f"\n=== [TURNO DE {e.name}] ===".upper())
                    start_turn_announce = TurnHandler.get_turn_announcement(e)
                    print(f"{start_turn_announce}")
                    print(f"❤️ {e.name} - HP: {e.hp}/{e.max_hp} | 🛡️ {e.name} - (+{e.damage_reduction * 100:.2f}%)")
                else:
                    print(f"\n=== [TURNO DOS INIMIGOS] ===")
                for e in active_enemies:
                    if player.is_alive:
                        CombatService.execute_turn(e, player)
                        time.sleep(1)

        player.in_combat = False

        # --- FIM DE JOGO ---
        if not player.is_alive:
            print(f"\n💀 {player.name} foi consumido pela escuridão... Fim de jogo.")
            GameState.set("active", False)
            sys.exit()