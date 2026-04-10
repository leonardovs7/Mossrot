import random

class CombatHandler:
    @staticmethod
    def attack(attacker) -> int:
        #retorna o dano do ataque + sorte
        luck = random.randint(0, 2)
        return attacker.base_damage + luck

    @staticmethod
    def defend(attacker, defender, raw_damage: int) -> None:
        # 1. Cálculo da mitigação
        # Se is_defending for True, dobra a capacidade de redução de dano
        multiplier = 2.0 if getattr(defender, 'is_defending', False) else 1.0
        effective_reduction = defender.damage_reduction * multiplier

        # Garante que a redução não passe de 100% (1.0)
        effective_reduction = min(1.0, effective_reduction)

        # 2. Aplicação do dano
        reduction_amount = raw_damage * effective_reduction
        final_damage = int(max(0, raw_damage - reduction_amount))

        defender.hp = max(0, defender.hp - final_damage)

        # 3. Feedback visual
        if reduction_amount > 0:
            print(f"\n>> {attacker.name} desfere um golpe forte, porém {defender.name} mitiga {int(reduction_amount)} pontos de dano e recebe {final_damage} de dano final! - ({defender.name} - HP: {defender.hp}/{defender.max_hp})")
        else:
            print(f"\n>> {attacker.name} desfere um golpe e {defender.name} recebe {final_damage} de dano! - ({defender.name} - HP: {defender.hp}/{defender.max_hp})")

        # 4. Reset do estado (Considere se deve ser aqui ou no fim do turno)
        defender.is_defending = False

    @staticmethod
    def passive_effect(attacker, defender) -> None:
        """Aplica dano passivo e retorna o feedback"""
        passive_bonus = getattr(attacker, 'current_weapon_bonus', 0)
        if passive_bonus > 0 and defender.is_alive:
            defender.hp = max(0, defender.hp - passive_bonus)

            weapon = getattr(attacker, 'equipped_weapon', None)
            item_subcategory = getattr(weapon, 'subcategory', None)

            if item_subcategory == "poison":
                feedback = f"\n🐍 O veneno do {attacker.weapon} queima as feridas de {defender.name}!"
            elif item_subcategory == "fire":
                feedback = f"\n🔥 As chamas residuais cauterizam a carne de {defender.name}!"
            else:
                feedback = f"\nUm efeito residual de {attacker.weapon} atinge o alvo!"

            print(f"{feedback}\n"
                    f"> {defender.name} sofre +{passive_bonus} de dano extra! ({defender.name} - HP: {defender.hp}/{defender.max_hp})")