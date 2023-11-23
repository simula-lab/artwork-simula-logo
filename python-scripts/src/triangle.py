from polygon import Polygon


class Triangle(Polygon):
    def __init__(self, A, B, C):
        self.A, self.B, self.C = A, B, C
        super().__init__([A, B, C])
