import math
import random

import numpy as np
import shapely
import vsketch
import vpype
from vsketch import Vsketch
from shapely.geometry import LineString, MultiLineString, Point, Polygon
from shapely.affinity import rotate

patterns = [
    rotate(
        MultiLineString(
            [((i, 0), (i, 20)) for i in np.linspace(0, 28, 28 * 5)] +
            [((0, i), (28, i)) for i in np.linspace(0, 20, 20 * 5)]
        ),
        5
    ),

    rotate(
        MultiLineString(
            [((i, 0), (i, 20)) for i in np.linspace(0, 28, 28 * 10)]
        ),
        5
    ),

    rotate(
        shapely.ops.unary_union([
            Point(x, y).buffer(0.05)
            for x in np.linspace(0, 28, 28 * 4)
            for y in np.linspace(0, 20, 20 * 4)
        ]),
        5
    )
]

class PatternsSketch(vsketch.SketchClass):
    landscape = vsketch.Param(True)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", center=True, landscape=self.landscape)
        vsk.scale("1cm")

        shape = Point(12, 8).buffer(3).union(Point(16, 12).buffer(5))
        patterned = shape.intersection(random.choice(patterns)).union(shape.boundary)

        vsk.geometry(patterned)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")

if __name__ == "__main__":
    PatternsSketch.display()
