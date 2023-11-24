class Syamaguc:
    def __init__(self):
        self.__name = "syamaguc"

    @property
    def name(self):
        return self.__name

    def introduce(self):
        return f"My name is {self.name}"
