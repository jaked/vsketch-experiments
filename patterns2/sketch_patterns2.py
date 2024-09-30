import numpy as np
import vsketch
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import unary_union
from shapely.affinity import rotate, translate, scale

width = 28
height = 20


def horizontal(): return unary_union(
    [LineString([(0, y), (width, y)])
     for y in np.linspace(0, height, height * 10)]
)


def left(): return rotate(
    unary_union(
        [LineString([(x - width/2, - height / 2), (x - width/2, height * 3/2)])
            for x in np.linspace(0, width * 2, width * 20)]
    ),
    15
)


def right(): return rotate(
    unary_union(
        [LineString([(x - width/2, - height / 2), (x - width/2, height * 3/2)])
            for x in np.linspace(0, width * 2, width * 20)]
    ),
    -15
)


class Patterns2Sketch(vsketch.SketchClass):
    # Sketch parameters:
    # radius = vsketch.Param(2.0)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=True)
        vsk.scale("cm")
        boundary = Polygon([(0, 0), (width, 0), (width, height), (0, height)])

        moon = Point(22, 5).buffer(2)

        stars = translate(scale(unary_union([
            Point(x, y).buffer(0.3) for (x, y) in [
                (4, 0),
                (0, 3),
                (4.75, 6),
                (5, 5),
                (5.25, 4),
                (7, 4.5),
                (10, 6.5),
                (6.5, 7.5),
                (6.5, 10.5)
            ]
        ]), 0.5, 0.5, origin=(0, 0)), 5, 2)

        right_hills = unary_union([
            Polygon([
                (5, 16),
                (6, 9),
                (17.25, 16),
            ]),
            Polygon([
                (20, 16),
                (21, 11),
                (28, 13),
                (28, 16)
            ])
        ])

        left_hills = unary_union([
            Polygon([
                (0, 12),
                (6, 9),
                (5, 16),
                (0, 16)
            ]),
            Polygon([
                (13, 16),
                (21, 11),
                (20, 16)
            ])
        ]).difference(right_hills)

        road = Polygon([
            (12.5, 20),
            (15.5, 20),
            (16.5, 19),
            (17.125, 18),
            (17.5, 17),
            (17.5, 16),
            (17, 16),
            (16.75, 17),
            (16, 18),
            (15, 19)
        ])

        ground = Polygon([
            (0, 16),
            (28, 16),
            (28, 20),
            (0, 20)
        ]).difference(road)

        layer1 = boundary.difference(
            unary_union([moon, stars, right_hills]))
        layer2 = boundary.difference(unary_union(
            [ground, right_hills, road, translate(moon, -0.15, -0.15), translate(stars, -0.05, -0.05)]))
        layer3 = boundary.difference(unary_union(
            [ground, left_hills, translate(moon, 0.15, -0.15), translate(stars, 0.05, -0.05)]))

        geom = unary_union([
            layer1.boundary,
            layer2.boundary,
            layer3.boundary,
        ])

        geom = unary_union([
            horizontal().intersection(layer1),
            left().intersection(layer2),
            right().intersection(layer3),
        ])

        vsk.geometry(unary_union([
            geom,
            boundary.boundary,
            left_hills.boundary,
            right_hills.boundary,
            road.boundary
        ]))
        vsk.vpype("squiggles")

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("squiggles linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Patterns2Sketch.display()
