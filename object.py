class Object():
    Rect = None
    Color = (255, 255, 255)
    Velocity = [0, 0]
    Coordinates = [0, 0]
    def __init__(self, Rect):
        self.Coordinates = [Rect.x, Rect.y]
        self.Rect = Rect