# src/handlers/level_handler.py

class LevelHandler:

    @staticmethod
    def level_up(player):
        """Executa a subida de nível e melhora os atributos."""
        needed_xp = player.next_level_xp
        player.current_xp -= needed_xp

        # 2. Sobe o nível
        player.level += 1

        # 3. Evolução de Atributos
        player.max_hp += 5
        player.hp = player.max_hp  # Cura total ao upar
        player.base_damage += 1

        print("\n" + "⭐" * 15)
        print(f"NÍVEL AUMENTOU: {player.level}")
        print(f"Sua vontade se fortalece nas sombras...")
        print(f"Vida Máxima: {player.max_hp} (+5)")
        print(f"Dano Base:   {player.base_damage} (+1)")
        print(f"XP para o próximo: {player.next_level_xp}")
        print("⭐" * 15 + "\n")

    @staticmethod
    def earn_xp(player, amount: int):
        """Adiciona XP e verifica se houve level up (pode ser múltiplos)."""
        if amount <= 0:
            return

        player.current_xp += amount
        print(f"✨ {player.name} ganhou {amount} pontos de experiência.")

        while player.current_xp >= player.next_level_xp:
            LevelHandler.level_up(player)