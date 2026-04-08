class SporeService:
    @staticmethod
    def process_breathing(player, current_scene) -> list:
        """
        Deve ser chamado a cada movimento ou turno no SceneManager.
        Verifica se o ar é tóxico e causa dano.
        """
        feedback_messages = []

        if getattr(current_scene, 'type', None) == "moldy": #só vai ocorrer em scenes de mofo
            spore_index = getattr(current_scene, 'spore_index', 0) # pega o valor de mofo da sala
            raw_spore_damage_debt = max(1, int(spore_index / 10)) # dano vai ser 10% do valor de mofo da sala

            spore_damage_debt = min(raw_spore_damage_debt, player.hp - 1) #garante que o dano não mate o player

            if spore_damage_debt > 0: #se o player tomar dano
                player.hp -= spore_damage_debt
                player.spore_debt += spore_damage_debt #soma o dano tomado no spore_damage_debt

                if spore_damage_debt > 20:
                    msg = f"\n>>> ☣ Você tosse violentamente enquanto o limo invade suas vias aéreas!* (-{spore_damage_debt} HP) <<<"
                else:
                    msg = f"\n>>> ☣ O ar está pesado. Esporos de Limo irritam seus pulmões. (-{spore_damage_debt} HP) <<<"
                feedback_messages.append(msg)

            elif player.hp == 1:
                feedback_messages.append("\n>>> ☣ Seus pulmões queimam e o ar parece sólido. Você não aguenta muito mais tempo aqui. <<<")

        return feedback_messages

    @staticmethod
    def recover_breathe(player):
        if player.spore_debt > 0:
            old_hp = player.hp
            player.hp = min(player.max_hp, player.hp + player.spore_debt) # recupera o hp limitado ao max_hp

            actual_recovered = player.hp - old_hp #calcula quanto foi curado deverade para a msg
            player.spore_debt = 0

            return f"Você alcança ar puro. Seus pulmões se limpam e a queimação cessa. (+{actual_recovered} HP)"

        return None
