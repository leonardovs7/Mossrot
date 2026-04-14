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
        reducing_bonus = 0.2 if getattr(defender, 'is_defending', False) else 0.0
        effective_reduction = defender.damage_reduction + reducing_bonus * multiplier

        # Garante que a redução não passe de 100% (1.0)
        effective_reduction = min(1.0, effective_reduction)

        # 2. Aplicação do dano
        reduction_amount = raw_damage * effective_reduction
        final_damage = int(max(0, raw_damage - reduction_amount))

        defender.hp = max(0, defender.hp - final_damage)

        # 3. Feedback visual
        if reduction_amount > 0:
            print(f"\n>> {attacker.name} desfere um golpe forte, porém {defender.name} mitiga {int(reduction_amount)} pontos de dano e recebe {final_damage} de dano final!")
        else:
            print(f"\n>> {attacker.name} desfere um golpe e {defender.name} recebe {final_damage} de dano!")

        defender.is_defending = False