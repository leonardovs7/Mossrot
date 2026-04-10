class SceneBridge:
    _manager = None

    @classmethod
    def register(cls, manager_instance):
        #atrelar
        cls._manager = manager_instance

    @classmethod
    def open_inventory(cls, player):
        #acessa o inventario do manager registrado.
        if cls._manager:
            cls._manager.show_inventory(player)

    def open_status(cls, player):
        #acessa o status do manager registrado.
        if cls._manager:
            cls._manager.show_status(player)

    @classmethod
    def say(cls, text: str):
        #usa o type_text do sceneManager para digitar com delay
        if cls._manager:
            cls._manager.type_text(text)
        else:
            print(text)