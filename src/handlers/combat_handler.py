import random

class CombatHandler:
    @staticmethod
    def attack(attacker) -> int:
        # Adicionei uma variação mínima para o dano não ser estático
        bonus = random.randint(0, 3)
        return attacker.base_damage + bonus

    @staticmethod
    def defend(entity, raw_damage: int) -> None:
        # 1. Cálculo da mitigação
        # Se is_defending for True, dobra a capacidade de redução de dano
        multiplier = 2.0 if getattr(entity, 'is_defending', False) else 1.0
        effective_reduction = entity.damage_reduction * multiplier

        # Garante que a redução não passe de 100% (1.0)
        effective_reduction = min(1.0, effective_reduction)

        # 2. Aplicação do dano
        reduction_amount = raw_damage * effective_reduction
        final_damage = int(max(0, raw_damage - reduction_amount))

        entity.hp = max(0, entity.hp - final_damage)

        # 3. Feedback visual
        print(f">> {entity.name} recebe {final_damage} de dano!")
        if reduction_amount > 0:
            print(f">  Mitigou {int(reduction_amount)} de dano! (HP: {entity.hp}/{entity.max_hp})\n")

        # 4. Reset do estado (Considere se deve ser aqui ou no fim do turno)
        entity.is_defending = False