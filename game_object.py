class GameObject():
    def __init__(self):
        self.health = 0
        self.damage = 0
    def hit(self, damage=1):
        self.health -= damage
