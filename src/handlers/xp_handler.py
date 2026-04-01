# src/handlers/level_handler.py

class LevelHandler:

    @staticmethod
    def level_up(player):
        """Executa a subida de nível e melhora os atributos."""
        # 1. Descontamos o custo do nível ATUAL antes de subir o nível
        # (Importante fazer isso antes de mudar o self.level, 
        # pois a property next_level_xp mudará de valor em seguida)
        xp_necessario = player.next_level_xp
        player.current_xp -= xp_necessario

        # 2. Sobe o nível
        player.level += 1

        # 3. Evolução de Atributos
        player.max_hp += 2
        player.hp = player.max_hp  # Cura total ao upar
        player.base_damage += 1

        print("\n" + "⭐" * 15)
        print(f"⭐ NÍVEL AUMENTOU: {player.level} ⭐")
        print(f"Sua vontade se fortalece nas sombras...")
        print(f"Vida Máxima: {player.max_hp} (+2)")
        print(f"Dano Base:   {player.base_damage} (+1)")
        print(f"XP para o próximo: {player.next_level_xp}")
        print("⭐" * 15 + "\n")

    @staticmethod
    def earn_xp(player, amount: int):
        """Adiciona XP e verifica se houve level up (pode ser múltiplos)."""
        if amount <= 0:
            return

        player.current_xp += amount
        print(f"✨ {player.name} absorveu {amount} de experiência.")

        # O 'while' é perfeito aqui: se o Leo ganhar muito XP (tipo de um Boss),
        # ele pode subir 2 ou 3 níveis de uma vez.
        while player.current_xp >= player.next_level_xp:
            LevelHandler.level_up(player)