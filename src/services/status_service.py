from src.models.enums import StatusEffect
from src.models.entities.item import Item

class StatusService:
    @staticmethod
    def apply_status(target, effect: StatusEffect, source_item: Item) -> str:
        """
        Aplica o efeito e usa o bônus do item como valor de dano.
        """
        if not target.is_alive or not source_item:
            return ""

        # O dano agora é dinâmico, vindo direto do bônus do item
        damage = source_item.passive_bonus
        target.hp = max(0, target.hp - damage)

        match effect:
            case StatusEffect.BLEEDING:
                return f"> {target.name} sofre +{damage} de dano por sangramento!"

            case StatusEffect.POISONED:
                return f"> O veneno de {source_item.name} queima as veias de {target.name} (-{damage} HP)."

            case StatusEffect.INFECTED:
                return f"> O mofo de {source_item.name} consome os tecidos de {target.name} (-{damage} HP)!"

            case StatusEffect.FOCUSED:
                return f"> {target.name} ignora a dor e mantém o foco."

            case _:
                return f"> Um efeito residual de {source_item.name} atinge {target.name} (-{damage} HP)."