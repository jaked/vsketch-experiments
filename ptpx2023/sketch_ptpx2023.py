import vsketch
import numpy as np
import shapely
import math

def circles_intersect(c1, c2):
    x1, y1, r1 = c1
    x2, y2, r2 = c2
    dist = (x1 - x2)**2 + (y1 - y2)**2
    return dist < (r1 + r2)**2

class Ptpx2023Sketch(vsketch.SketchClass):
    # Sketch parameters:
    x_points = vsketch.Param(220, 10, 500)
    y_points = vsketch.Param(140, 10, 500)
    slant = vsketch.Param(0.25, 0, 1.0)
    tails = vsketch.Param(5, 0, 10)
    box = vsketch.Param(True)
    magnitude = vsketch.Param(0.01, 0, 1.0)
    scale = vsketch.Param(20, 0, 50)
    num_stars = vsketch.Param(90, 0, 500)
    min_radius = vsketch.Param(0.1, 0, 1.0)
    max_radius = vsketch.Param(0.2, 0, 1.0)

    border = shapely.geometry.box(0.25, 0.25, 5.75, 3.75)

    def star(self, vsk):
        xoff = vsk.random(6)
        yoff = vsk.random(4)
        r = vsk.random(self.min_radius, self.max_radius)
        thoff = vsk.random(math.pi)
        length = vsk.random(r * self.tails, r * self.tails * 2)
        star_points = []
        for i in range(10):
            th = thoff + i * 2 * math.pi / 10
            x = math.cos(th)
            y = math.sin(th)
            if (i % 2 == 0):
                x *= r / 4
                y *= r / 4
            else:
                x *= r
                y *= r
            star_points.append((x + xoff, y + yoff))
        # slant more toward the top
        # slant more left if closer to the left edge
        # and more right if closer to the right edge
        slant = (xoff - 3 + vsk.random(-0.5, 0.5)) * (1 - (yoff - length) / 4) * self.slant
        tail_points = [
            (xoff - r / 8, yoff),
            (xoff - slant - r / 16, yoff - length),
            (xoff - slant + r / 16, yoff - length),
            (xoff + r / 8, yoff),
        ]
        return [shapely.Polygon(star_points), shapely.Polygon(tail_points)]

    def stars(self, vsk, count):
        stars = []
        for i in range(count):
            again = True
            while again:
                [star, tail] = self.star(vsk)
                startail = star.union(tail)
                if (all(startail.disjoint(s) for s in stars) and (not self.box or star.within(self.border))):
                    stars.append(startail)
                    again = False
        return stars

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("6in", "4in", center=False)
        vsk.scale("inch")

        x_range = np.linspace(0.25, 5.75, self.x_points)
        y_range = np.linspace(0.25, 3.75, self.y_points)
        xs, ys = np.meshgrid(x_range, y_range)
        grid = np.vectorize(complex)(xs, ys)
        noise = (0.5 - vsk.noise(y_range * self.scale, x_range * self.scale)) * self.magnitude
        noise = np.vectorize(complex)(noise, noise)
        points = np.vectorize(lambda c: shapely.Point(c.real, c.imag))(grid + noise)

        lines = shapely.MultiLineString([shapely.LineString(row) for row in points])
        stars = shapely.union_all(self.stars(vsk, self.num_stars))

        vsk.geometry(lines.difference(stars))

    def finalize(self, vsk: vsketch.Vsketch) -> None:
#        vsk.vpype("linemerge linesimplify reloop linesort")
        vsk.vpype("linemerge linesimplify")


if __name__ == "__main__":
    Ptpx2023Sketch.display()
