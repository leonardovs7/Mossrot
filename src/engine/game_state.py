class GameState:
    _flags = {}

    @staticmethod
    def set(key: str, value: any):
        """Define ou atualiza uma informação no jogo."""
        GameState._flags[key] = value

    @staticmethod
    def get(key: str, default=False) -> any:
        """Recupera uma informação. Se não existir, retorna o 'default'."""
        return GameState._flags.get(key, default)

    @staticmethod
    def show_debug():
        """Útil para você ver o que está acontecendo por baixo dos panos."""
        print(f"\n--- DEBUG STATUS ---")
        for k, v in GameState._flags.items():
            print(f"{k}: {v}")
        print("--------------------\n")