import time
import sys
import random
from typing import List, Union

from src.engine.scene_bridge import SceneBridge
from src.handlers.turn_handler import TurnHandler
from src.handlers.xp_handler import LevelHandler
from src.models.entities.entity import Entity
from src.models.entities.player import Player
from src.models.entities.enemy import Enemy
from src.handlers.combat_handler import CombatHandler


class CombatService:
    @staticmethod
    def execute_turn(attacker: Entity, defender: Entity, skip_menu: bool = False):
        attacker.is_defending = False

        if isinstance(attacker, Player) and not skip_menu:
            print("\n" + "=" * 45)
            print(f"\n[ TURNO DE {attacker.name} ]")
            start_turn_announce = TurnHandler.get_turn_announcement(attacker)
            print(f"'{start_turn_announce}'")
            print(f"❤️ HP: {attacker.hp}/{attacker.max_hp} | 🗡️ {attacker.weapon} (+{attacker.current_weapon_damage}) | 🛡️ {attacker.armor} (+{attacker.current_armor_defense * 100}%)")
            print("\n1 - Atacar | 2 - Defender | 3 - Defender")

            choice = input("Escolha sua ação: \n> ")

            if choice == "1":
                pass

            elif choice == "2":
                attacker.is_defending = True
                print(f"🛡️ {attacker.name} entrou em postura defensiva!")
                return

            elif choice == "3":
                SceneBridge.open_inventory(attacker)
                return

            else:
                return CombatService.execute_turn(attacker, defender)

        # 1. Gerar dano usando o CombatHandler
        raw_damage = CombatHandler.attack(attacker)

        # 2. Aplicar dano e mitigação usando o CombatHandler
        CombatHandler.defend(attacker, defender, raw_damage)

        #3. Adicionar lógica de dano passivo por status
        CombatHandler.passive_effect(attacker, defender)

        time.sleep(1)

    @staticmethod
    def start_combat(player: Player, enemies: Union[Enemy, List[Enemy]], is_surprise: bool = False):
        player.in_combat = True
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

                print(f"❤️ HP: {player.hp}/{player.max_hp} | 🗡️ {player.weapon} (+{player.current_weapon_damage}) | 🛡️ {player.armor} (+{player.current_armor_defense})")
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
                if len(active_enemies) == 1:
                    print("\n" + "=" * 45)
                    print(f"\n[ TURNO DE {e.name} ]")
                    start_turn_announce = TurnHandler.get_turn_announcement(e)
                    print(f"'{start_turn_announce}'")
                    print(f"❤️ {e.name} - HP: {e.hp}/{e.max_hp} | 🛡️ {e.name} - (+{e.damage_reduction * 100}%)")
                else:
                    print("\n" + "=" * 45)
                    print(f"\n[ TURNO DOS INIMIGOS ]")
                    start_turn_announce = TurnHandler.get_turn_announcement(e)
                    print(f"'{start_turn_announce}'")
                    print(f"❤️ {e.name} - HP: {e.hp}/{e.max_hp} | 🛡️ {e.name} - (+{e.damage_reduction * 100}%)")
                for e in active_enemies:
                    if player.is_alive:
                        CombatService.execute_turn(e, player)
                        time.sleep(0.5)

        player.in_combat = False

        # --- FIM DE JOGO ---
        if not player.is_alive:
            print(f"\n💀 {player.name} foi consumido pela escuridão... Fim de jogo.")
            sys.exit()