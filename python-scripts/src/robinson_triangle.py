from triangle import Triangle


class RobinsonTriangle(Triangle):
    """
    A class representing a Robinson triangle and the rhombus formed from it.

    """

    def __init__(self, A, B, C):
        """
        Initialize the triangle with the ordered vertices. A and C are the
        vertices at the equal base angles; B is at the vertex angle.

        """

        super().__init__(A, B, C)

    def centre(self):
        """
        Return the position of the centre of the rhombus formed from two
        triangles joined by their bases.

        """

        return (self.A + self.C) / 2

    def path(self, rhombus=True):
        """
        Return the SVG "d" path element specifier for the rhombus formed
        by this triangle and its mirror image joined along their bases. If
        rhombus=False, the path for the triangle itself is returned instead.

        """

        AB, BC = self.B - self.A, self.C - self.B
        xy = lambda v: (v.real, v.imag)
        if rhombus:
            return "m{},{} l{},{} l{},{} l{},{}z".format(
                *xy(self.A) + xy(AB) + xy(BC) + xy(-AB)
            )
        return "m{},{} l{},{} l{},{}z".format(*xy(self.A) + xy(AB) + xy(BC))

    def get_arc_d(self, U, V, W, half_arc=False):
        """
        Return the SVG "d" path element specifier for the circular arc between
        sides UV and UW, joined at half-distance along these sides. If
        half_arc is True, the arc is at the vertex of a rhombus; if half_arc
        is False, the arc is drawn for the corresponding vertices of a
        Robinson triangle.

        """

        start = (U + V) / 2
        end = (U + W) / 2
        # arc radius
        r = abs((V - U) / 2)

        if half_arc:
            # Find the endpoint of the "half-arc" terminating on the triangle
            # base
            UN = V + W - 2 * U
            end = U + r * UN / abs(UN)

        # ensure we draw the arc for the angular component < 180 deg
        cross = lambda u, v: u.real * v.imag - u.imag * v.real
        US, UE = start - U, end - U
        if cross(US, UE) > 0:
            start, end = end, start
        return "M {} {} A {} {} 0 0 0 {} {}".format(
            start.real, start.imag, r, r, end.real, end.imag
        )

    def arcs(self, half_arc=False):
        """
        Return the SVG "d" path element specifiers for the two circular arcs
        about vertices A and C. If half_arc is True, the arc is at the vertex
        of a rhombus; if half_arc is False, the arc is drawn for the
        corresponding vertices of a Robinson triangle.

        """

        D = self.A - self.B + self.C
        arc1_d = self.get_arc_d(self.A, self.B, D, half_arc)
        arc2_d = self.get_arc_d(self.C, self.B, D, half_arc)
        return arc1_d, arc2_d

    def conjugate(self):
        """
        Return the vertices of the reflection of this triangle about the
        x-axis. Since the vertices are stored as complex numbers, we simply
        need the complex conjugate values of their values.

        """

        return self.__class__(
            self.A.conjugate(), self.B.conjugate(), self.C.conjugate()
        )
