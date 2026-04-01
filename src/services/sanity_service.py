class SanityService:

    @staticmethod
    def reduce_sanity(player, amount: int) -> str:
        old_player_sanity = player.sanity
        player.sanity = max(0, player.sanity - amount)
        return f"Você se sente tonto, parece que a grama puxa seu pé.. Sua sanidade caiu {amount} pontos! - Atual: {player.sanity}/{old_player_sanity}"

    @staticmethod
    def increase_sanity(player, amount: int) -> str:
        old_player_sanity = player.sanity
        player.sanity = min(100, player.sanity + amount)
        return f"Você sente uma confiança inesperada.. Sua sanidade aumentou {amount} pontos! - Atual: {player.sanity}/{old_player_sanity}"
