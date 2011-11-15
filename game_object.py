"""
Game Object
"""

class GameObject():
    """Game object"""
    def __init__(self):
        self.health = 0
        self.damage = 0
        self.point_value = 0

    def hit(self, damage=1):
        """defines hit function"""
        self.health -= damage

    def die(self):
        """Death"""
        return self.point_value