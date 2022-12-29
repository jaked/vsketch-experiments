import random

import numpy as np
import shapely
import vsketch
from vsketch import Vsketch
from shapely.geometry import MultiLineString, Point, Polygon
from shapely.affinity import rotate

class RectsSketch(vsketch.SketchClass):
    landscape = vsketch.Param(True)
    numrects = vsketch.Param(200)
    maxscale = vsketch.Param(5)
    mode = vsketch.Param("linear", choices=vsketch.EASING_FUNCTIONS.keys())
    low_deadzone = vsketch.Param(0.0, 0.0, 100.0, step=5)
    high_deadzone = vsketch.Param(0.0, 0.0, 100.0, step=5)
    skew = vsketch.Param(0, 0, 180)
    radius = vsketch.Param(0.45)
    gap = vsketch.Param(0.04)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=self.landscape)
        vsk.scale("cm")

        width, height = (28, 20) if self.landscape else (20, 28)
        border = Polygon([(0, 0), (0, height), (width, height), (width, 0)])

        def make_rect(i):
            maxscale = int(Vsketch.easing(
                value=i,
                mode=self.mode,
                low_dead=self.low_deadzone / 100.0,
                high_dead=self.high_deadzone / 100.0,
                start1=0,
                stop1=self.numrects,
                start2=self.maxscale,
                stop2=1,
            ))
            scale = (random.randint(1, maxscale), random.randint(1, maxscale))
            offset = (random.randrange(0, width), random.randrange(0, height))
            return shapely.transform(
                Polygon([(0, 0), (0, 1), (1, 1), (1, 0)]),
                lambda p: p * scale + offset)

        # generate rects first then rotate so adjusting the skew parameter doesn't move the rects
        rects = [
            rotate(rect, random.randint(-self.skew, self.skew))
            for rect in [ make_rect(i) for i in range(self.numrects)]
        ]

        for (i, rect) in enumerate(rects):
            for other in rects[i+1:]:
                rect = rect.difference(other)
            geom = rect.intersection(border).buffer(-(self.gap + self.radius)).buffer(self.radius)
            vsk.geometry(geom)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    RectsSketch.display()
