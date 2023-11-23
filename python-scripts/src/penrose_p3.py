import math
import random

from btiles import BtileL

# A small tolerance for comparing floats for equality
TOL = 1.0e-5
# psi = 1/phi where phi is the Golden ratio, sqrt(5)+1)/2
psi = (math.sqrt(5) - 1) / 2


class PenroseP3:
    """A class representing the P3 Penrose tiling."""

    def __init__(self, scale=200, ngen=4, config={}):
        """
        Initialise the PenroseP3 instance with a scale determining the size
        of the final image and the number of generations, ngen, to inflate
        the initial triangles. Further configuration is provided through the
        key, value pairs of the optional config dictionary.

        """

        self.scale = scale
        self.ngen = ngen

        # Default configuration
        self.config = {
            "width": "100%",
            "height": "100%",
            "stroke-colour": "#fff",
            "base-stroke-width": 0.05,
            "margin": 1.05,
            "tile-opacity": 0.6,
            "random-tile-colours": False,
            "Stile-colour": "#08f",
            "Ltile-colour": "#0035f3",
            "Aarc-colour": "#f00",
            "Carc-colour": "#00f",
            "draw-tiles": True,
            "draw-arcs": False,
            "reflect-x": True,
            "draw-rhombuses": True,
            "rotate": 0,
            "flip-y": False,
            "flip-x": False,
        }
        self.config.update(config)
        # And ensure width, height values are strings for the SVG
        self.config["width"] = str(self.config["width"])
        self.config["height"] = str(self.config["height"])

        self.elements = []

    def set_initial_tiles(self, tiles):
        self.elements = tiles

    def inflate(self):
        """ "Inflate" each triangle in the tiling ensemble."""
        new_elements = []
        for element in self.elements:
            new_elements.extend(element.inflate())
        self.elements = new_elements

    def remove_dupes(self):
        """
        Remove triangles giving rise to identical rhombuses from the
        ensemble.

        """

        # Triangles give rise to identical rhombuses if these rhombuses have
        # the same centre.
        selements = sorted(
            self.elements, key=lambda e: (e.centre().real, e.centre().imag)
        )
        self.elements = [selements[0]]
        for i, element in enumerate(selements[1:], start=1):
            if abs(element.centre() - selements[i - 1].centre()) > TOL:
                self.elements.append(element)

    def add_conjugate_elements(self):
        """Extend the tiling by reflection about the x-axis."""

        self.elements.extend([e.conjugate() for e in self.elements])

    def rotate(self, theta):
        """Rotate the figure anti-clockwise by theta radians."""

        rot = math.cos(theta) + 1j * math.sin(theta)
        for e in self.elements:
            e.A *= rot
            e.B *= rot
            e.C *= rot

    def flip_y(self):
        """Flip the figure about the y-axis."""

        for e in self.elements:
            e.A = complex(-e.A.real, e.A.imag)
            e.B = complex(-e.B.real, e.B.imag)
            e.C = complex(-e.C.real, e.C.imag)

    def flip_x(self):
        """Flip the figure about the x-axis."""

        for e in self.elements:
            e.A = e.A.conjugate()
            e.B = e.B.conjugate()
            e.C = e.C.conjugate()

    def make_tiling(self):
        """Make the Penrose tiling by inflating ngen times."""

        for gen in range(self.ngen):
            self.inflate()
        if self.config["draw-rhombuses"]:
            self.remove_dupes()
        if self.config["reflect-x"]:
            self.add_conjugate_elements()
            self.remove_dupes()

        # Rotate the figure anti-clockwise by theta radians.
        theta = self.config["rotate"]
        if theta:
            self.rotate(theta)

        # Flip the image about the y-axis (note this occurs _after_ any
        # rotation.
        if self.config["flip-y"]:
            self.flip_y()

        # Flip the image about the x-axis (note this occurs _after_ any
        # rotation and after any flip about the y-axis.
        if self.config["flip-x"]:
            self.flip_x()

    def get_tile_colour(self, e):
        """Return a HTML-style colour string for the tile."""

        if self.config["random-tile-colours"]:
            # Return a random colour as '#xxx'
            return "#" + hex(random.randint(0, 0xFFF))[2:]

        # Return the colour string, or call the colour function as appropriate
        if isinstance(e, BtileL):
            if hasattr(self.config["Ltile-colour"], "__call__"):
                return self.config["Ltile-colour"](e)
            return self.config["Ltile-colour"]

        if hasattr(self.config["Stile-colour"], "__call__"):
            return self.config["Stile-colour"](e)
        return self.config["Stile-colour"]

    def make_svg(self):
        """Make and return the SVG for the tiling as a str."""

        xmin = ymin = -self.scale * self.config["margin"]
        width = height = 2 * self.scale * self.config["margin"]
        viewbox = "{} {} {} {}".format(xmin, ymin, width, height)
        svg = [
            '<?xml version="1.0" encoding="utf-8"?>',
            '<svg width="{}" height="{}" viewBox="{}"'
            ' preserveAspectRatio="xMidYMid meet" version="1.1"'
            ' baseProfile="full" xmlns="http://www.w3.org/2000/svg">'.format(
                self.config["width"], self.config["height"], viewbox
            ),
        ]
        # The tiles' stroke widths scale with ngen
        stroke_width = str(
            psi**self.ngen * self.scale * self.config["base-stroke-width"]
        )
        svg.append(
            '<g style="stroke:{}; stroke-width: {};'
            ' stroke-linejoin: round;">'.format(
                self.config["stroke-colour"], stroke_width
            )
        )
        draw_rhombuses = self.config["draw-rhombuses"]
        for e in self.elements:
            if self.config["draw-tiles"]:
                svg.append(
                    '<path fill="{}" fill-opacity="{}" d="{}"/>'.format(
                        self.get_tile_colour(e),
                        self.config["tile-opacity"],
                        e.path(rhombus=draw_rhombuses),
                    )
                )
            if self.config["draw-arcs"]:
                arc1_d, arc2_d = e.arcs(half_arc=not draw_rhombuses)
                svg.append(
                    '<path fill="none" stroke="{}" d="{}"/>'.format(
                        self.config["Aarc-colour"], arc1_d
                    )
                )
                svg.append(
                    '<path fill="none" stroke="{}" d="{}"/>'.format(
                        self.config["Carc-colour"], arc2_d
                    )
                )
        svg.append("</g>\n</svg>")
        return "\n".join(svg)

    def write_svg(self, filename):
        """Make and write the SVG for the tiling to filename."""
        svg = self.make_svg()
        with open(filename, "w") as fo:
            fo.write(svg)
