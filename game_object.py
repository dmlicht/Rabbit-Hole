class GameObject():
    def __init__(self):
        self.health = 0
        self.damage = 0
        self.point_value = 0
        self.invincible = 0

    def hit(self, damage=1):
        self.health -= damage

    def die(self, level):
        return self.point_value

    def fire(self, level):
        return False