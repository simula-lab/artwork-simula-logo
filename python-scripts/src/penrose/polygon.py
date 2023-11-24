class Polygon:
    def __init__(self, vertices):
        self.vertices = vertices

    @property
    def n(self):
        return len(self.vertices)
