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
    x_points = vsketch.Param(165, 10, 500)
    y_points = vsketch.Param(105, 10, 500)
    magnitude = vsketch.Param(0.02, 0, 1.0)
    scale = vsketch.Param(10, 0, 20)
    stars = vsketch.Param(10, 0, 500)
    min_radius = vsketch.Param(0.1, 0, 1.0)
    max_radius = vsketch.Param(0.5, 0, 1.0)

    def star(self, xoff, yoff, r, thoff):
        points = []
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
            points.append((x + xoff, y + yoff))
        return shapely.Polygon(points)

    def circles(self, vsk, count):
        circles = []
        for i in range(count):
            again = True
            while again:
                x = vsk.random(6)
                y = vsk.random(4)
                r = vsk.random(self.min_radius, self.max_radius)
                circle = (x, y, r)
                if (not any([circles_intersect(circle, c) for c in circles])):
                    circles.append(circle)
                    again = False
        return circles

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
        circles = shapely.union_all([shapely.Point(x, y).buffer(r) for (x, y, r) in self.circles(vsk, self.stars)])
        stars = shapely.union_all([self.star(x, y, r, vsk.random(math.pi)) for (x, y, r) in self.circles(vsk, self.stars)])

        vsk.geometry(lines.difference(stars))

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Ptpx2023Sketch.display()
