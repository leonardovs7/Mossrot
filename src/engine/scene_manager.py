import time
import sys
import random
from typing import List

from src.services.inventory_service import InventoryService
from src.services.combat_service import CombatService
from src.handlers.shadow_ambush_handler import ShadowAmbushHandler
from src.models.entities.item import LightEquipment
from src.services.light_service import LightService

class SceneManager:
    def __init__(self, scenes: List['GameScene'], start_id: str):
        self.scenes = {s.id: s for s in scenes}
        self.current_scene = self.scenes[start_id]

    def type_text(self, text: str):
        if not text: return
        for x in text:
            sys.stdout.write(x)
            sys.stdout.flush()
            #delay = random.uniform(0.01, 0.03)
            delay = 0.00
            time.sleep(delay)  # Um delay mínimo para o efeito
        print()

    def display_scene(self, player):
        while True:
            self.type_text(f"\n=== {self.current_scene.title} ===\n")

            description = self.current_scene.description
            if callable(description):
                self.type_text(description(player))
            else:
                self.type_text(description)

            # Evento ao entrar na cena
            if self.current_scene.on_enter:
                action = self.current_scene.on_enter
                if not getattr(self.current_scene, "on_enter_repeatable", False):
                    self.current_scene.on_enter = None

                feedback = action(player)
                if isinstance(feedback, str):
                    if feedback in self.scenes:
                        self.current_scene = self.scenes[feedback]
                        continue
                    else:
                        self.type_text(feedback)
                        input("\n[Pressione Enter para continuar...]")

            # Filtrar opções válidas
            valid_options = []
            print("O que você vai fazer agora?\n")
            for opt in self.current_scene.options:
                if not opt.requirement or opt.requirement(player):
                    if opt.only_once and opt.is_used:
                        continue
                    valid_options.append(opt)

            for i, opt in enumerate(valid_options, 1):
                print(f"{i}. {opt.text}")

            return valid_options

    def move_scene(self, target_id: str, player):
        if target_id in self.scenes:
            target = self.scenes[target_id]


            # Lógica de Caverna/Escuridão
            if hasattr(target, 'type') and target.type == "cave":
                # Consome combustível da lamparina se trocar de cena
                feedbacks = LightService.process_consume(player)
                if feedbacks:
                    for msg in feedbacks:
                        self.type_text(msg)

                # Se não tem luz (atributo do Player), gera emboscada
                if not getattr(player, 'has_light', False):
                    ShadowAmbushHandler.trigger_shadow_ambush(player)

            if player.is_alive:
                self.current_scene = target
        else:
            print(f"❌ ERRO: Cena {target_id} não encontrada!")

    def show_inventory(self, player):
        print("\n[INVENTÁRIO]")
        if not player.inventory:
            self.type_text("Suas mãos estão vazias...")
            return

        for i, item in enumerate(player.inventory, 1):
            print(f"{i} - {item.name} [{item.category}]")

        print("\n[EQUIPAMENTOS]")
        print(f"🗡️ Arma: {player.weapon} (+{player.current_weapon_bonus})")
        print(f"🛡️ Armadura: {player.armor} (+{player.current_armor_bonus})")
        print("\n[0] Voltar | [ID] Examinar")

        try:
            choice = input("> ")
            if choice == "0": return

            idx = int(choice) - 1
            if 0 <= idx < len(player.inventory):
                item = player.inventory[idx]
                self.type_text(f"\n>> {item.name}: {item.description}")
                print("\n[1] Usar/Equipar | [2] Sair")

                opt = input("> ")
                if opt == "1":
                    feedback = InventoryService.use(player, item)
                    if feedback:
                        self.type_text(feedback)
                    input("\n[Pressione Enter para continuar...]")
        except (ValueError, IndexError):
            pass

    def show_status(self, player):
        # Busca lamparina para mostrar o fuel
        light_item = next((i for i in player.inventory if isinstance(i, LightEquipment)), None)
        fuel = f"{light_item.fuel:.1f}/{light_item.max_fuel}" if light_item else "N/A"

        status_msg = (
            f"\n--- STATUS DE {player.name} ---\n"
            f"❤️ Vida: {player.hp}/{player.max_hp}\n"
            f"🗡️ Dano: {player.base_damage}\n"
            f"🛡️ Armadura: {player.damage_reduction}\n"
            f"🔥 Combustível: {fuel}\n"
            f"🧠 Sanidade: {player.sanity}/{player.max_sanity}\n"
            f"🌟 Level: {player.level} (XP: {player.current_xp}/{player.next_level_xp})"
        )
        print(status_msg)
        input("\n[Pressione Enter para continuar...]")

    def navigate(self, player):
        while player.is_alive:
            options = self.display_scene(player)
            if not options: break

            print("\nDigite o número, 'i' para ir ao Inventário ou 's' para ver suas Estatísticas")
            entrada = input("> ").lower().strip()

            if entrada in ['i', 'inv', 'inventario']:
                self.show_inventory(player)
                continue
            elif entrada in ['s', 'stat', 'status']:
                self.show_status(player)
                continue

            try:
                choice = int(entrada) - 1
                if 0 <= choice < len(options):
                    selected = options[choice]

                    if selected.action:
                        feedback = selected.action(player)
                        if isinstance(feedback, str):
                            self.type_text(feedback)

                    selected.is_used = True
                    self.move_scene(selected.target_scene_id, player)
                else:
                    print("❌ Opção inválida.")
            except ValueError:
                print("❌ Comando inválido.")

        if not player.is_alive:
            print("\n💀 A escuridão finalmente te alcançou...")
            sys.exit()