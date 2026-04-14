import time
import sys
import os
import random
from typing import List
from src.engine.game_state import GameState
from src.engine.scene_bridge import SceneBridge
from src.models.enums import SceneType
from src.services.inventory_service import InventoryService
from src.handlers.shadow_ambush_handler import ShadowAmbushHandler
from src.models.entities.item import LightEquipment
from src.services.light_service import LightService
from src.services.spore_service import SporeService

class SceneManager:
    def __init__(self, scenes: List['GameScene'], start_id: str):
        self.scenes = {s.id: s for s in scenes}
        self.current_scene = self.scenes[start_id]
        SceneBridge.register(self)

    def type_text(self, text: str):
        if not text: return
        for x in text:
            sys.stdout.write(x)
            sys.stdout.flush()
            #delay = random.uniform(0.02, 0.06)
            #time.sleep(delay)
        print()

    def display_scene(self, player):
        os.system('cls' if os.name == 'nt' else 'clear')
        while True:
            if self.current_scene.type == SceneType.MOLDY:
                spore_perc = getattr(self.current_scene, 'spore_index', 0)
                self.type_text(f"\n=== {self.current_scene.title} - [{spore_perc}% Contaminado] ===\n".upper())
            else:
                self.type_text(f"\n=== {self.current_scene.title} ===\n".upper())

            description = self.current_scene.description
            if callable(description):
                self.type_text(description(player))
            else:
                self.type_text(description)

            # Evento ao entrar na cena
            if self.current_scene.on_enter: #se existe o evento de on_enter na cena
                action = self.current_scene.on_enter #define a action do on_enter
                if not getattr(self.current_scene, "on_enter_repeatable", False): #se o en_enter_repeatable for true >
                    self.current_scene.on_enter = None #define o on_enter como None para não reproduzir novamente
                feedback = action(player) #pega o retorno da action
                if isinstance(feedback, str): #se a action retornar uma str
                    if feedback in self.scenes: #se o retorno da action for uma scene
                        self.current_scene = self.scenes[feedback] #muda a cena para o retorno da ação
                        os.system('cls' if os.name == 'nt' else 'clear') #limpa o console
                        continue
                    else: #se não for uma scene
                        self.type_text(feedback) #digita com efeito o retorno da action
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

            if self.current_scene and self.current_scene.id != target_id:
                # Só reseta se o foco estava ligado
                if GameState.get("focus_active"):
                    GameState.set("focus_active", False, immutable=False)
                    self.type_text("\n👁️ Sua concentração se quebra ao mudar de ambiente...")
                    input("\n[Pressione Enter para continuar...]")

                # Só recupera a respiração se sair da área mofada
                if self.current_scene.type == SceneType.MOLDY and target.type != SceneType.MOLDY:
                    recovery_msg = SporeService.recover_breathe(player)
                    if recovery_msg:
                        self.type_text(recovery_msg)
                        input("\n[Pressione Enter para continuar...]")

            # Lógica de Caverna/Escuridão
            match target.type:
                case SceneType.DARK:
                    # Consome combustível e checa se está acesa (Luz)
                    feedbacks = LightService.process_consume(player)
                    if feedbacks:
                        for msg in feedbacks:
                            self.type_text(msg)

                # Se não tem luz (atributo do Player), gera emboscada
                    if not any(getattr(i, 'is_lit', False) for i in player.inventory):
                        ShadowAmbushHandler.trigger_shadow_ambush(player)

            # Lógica de Áreas Mofadas
                case SceneType.MOLDY:
                    # Processa a respiração e acúmulo de esporos
                    feedbacks = SporeService.process_breathing(player, target)
                    if feedbacks:
                        for msg in feedbacks:
                            self.type_text(msg)

                case SceneType.NORMAL:
                    pass

            if player.is_alive:
                self.current_scene = target
                GameState.set("last_scene", target.id)

        else:
            print(f"ERRO: Cena {target_id} não encontrada!")

    def show_inventory(self, player):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n[INVENTÁRIO]")
            if not player.inventory:
                self.type_text("Suas mãos estão vazias...")
                input("\n[Pressione Enter para continuar...]")
                return

            for i, item in enumerate(player.inventory, 1):
                name_and_quantity = f"({item.quantity}x) {item.name}"
                print(f"{i} - {name_and_quantity:<40} [{item.category}]")

            print("\n[EQUIPAMENTOS]")
            print(f"🗡️ Arma: {player.weapon} (+{player.current_weapon_damage})")
            print(f"🛡️ Armadura: {player.armor} (+{player.current_armor_defense})")
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
                    elif opt == "2":
                        continue
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
            if not options:
                break

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
                    #processa a escolha
                    if selected.action:
                        feedback = selected.action(player)
                        if isinstance(feedback, str):
                            self.type_text(feedback)
                    input("\n[Pressione Enter para continuar...]")

                    selected.is_used = True
                    self.move_scene(selected.target_scene_id, player)

                else:
                    print("❌ Opção inválida.")
                    time.sleep(1)
            except ValueError:
                print("❌ Comando inválido.")
                time.sleep(1)

        if not player.is_alive:
            print("\n💀 A escuridão finalmente te alcançou...")
            sys.exit()