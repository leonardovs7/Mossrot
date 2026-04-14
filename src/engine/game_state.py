import sqlite3
import os


class GameState:
    # _flags agora guarda: { key: {'value': any, 'immutable': bool} }
    _flags = {}
    _db_path = "src/models/database/mossrot_state.sqlite"

    @staticmethod
    def init():
        """Inicializa o banco e carrega os estados, incluindo a trava de imutabilidade."""
        # Garante que a pasta existe antes de tentar abrir o banco
        os.makedirs(os.path.dirname(GameState._db_path), exist_ok=True)

        with sqlite3.connect(GameState._db_path) as conn:
            # Adicionamos a coluna is_immutable (0 para False, 1 para True)
            conn.execute("""
                         CREATE TABLE IF NOT EXISTS game_state
                         (
                             key TEXT PRIMARY KEY,
                             value ANY,
                             is_immutable INTEGER DEFAULT 1
                         )""")

            cursor = conn.execute("SELECT key, value, is_immutable FROM game_state")
            for key, value, is_immutable in cursor.fetchall():
                # Processamento de tipos booleanos do SQLite
                processed_value = value
                if value == 1:
                    processed_value = True
                elif value == 0:
                    processed_value = False

                GameState._flags[key] = {
                    'value': processed_value,
                    'immutable': bool(is_immutable)
                }

    @staticmethod
    def set(key: str, value, immutable: bool = False):
        """
        Define ou atualiza um valor.
        Impedirá a atualização se a chave já existir e for imutável.
        """
        # 1. Checa se a chave já existe e se está travada
        if key in GameState._flags and GameState._flags[key]['immutable']:
            print(f"⚠️ [GameState] ERRO: A chave '{key}' é imutável e não pode ser sobrescrita.")
            return False

        # 2. Atualiza a memória
        GameState._flags[key] = {
            'value': value,
            'immutable': immutable
        }

        # 3. Persiste no banco de dados
        with sqlite3.connect(GameState._db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO game_state (key, value, is_immutable) 
                VALUES (?, ?, ?)
            """, (key, value, 1 if immutable else 0))
        return True

    @staticmethod
    def get(key: str, default=False):
        """Retorna apenas o valor da chave."""
        data = GameState._flags.get(key)
        return data['value'] if data else default

    @staticmethod
    def delete(key: str):
        """
        Remove uma chave do banco e da memória, mesmo se for imutável.
        (Única forma de 'resetar' um valor imutável).
        """
        if key in GameState._flags:
            del GameState._flags[key]
            with sqlite3.connect(GameState._db_path) as conn:
                conn.execute("DELETE FROM game_state WHERE key = ?", (key,))
            print(f"🗑️ [GameState] Chave '{key}' removida com sucesso.")
            return True
        return False

    @staticmethod
    def clear_save():
        GameState._flags = {}
        if os.path.exists(GameState._db_path):
            os.remove(GameState._db_path)
        GameState.init()

    @staticmethod
    def show_debug():
        print(f"\n--- [ DEBUG GAME STATE ] ---")
        if not GameState._flags:
            print("Estado vazio.")
        for k, v in GameState._flags.items():
            status = "[IMUTÁVEL]" if v['immutable'] else "[FLEXÍVEL]"
            print(f"{status} {k:.<20} Value: {v['value']:<15} Type: {type(v['value']).__name__}")
        print("----------------------------\n")