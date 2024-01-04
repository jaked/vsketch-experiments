import vsketch


class Rect6x4Sketch(vsketch.SketchClass):
    # Sketch parameters:
    # radius = vsketch.Param(2.0)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("6in", "4in", landscape=False)
        vsk.scale("inch")

        vsk.rect(0, 0, 6, 4)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Rect6x4Sketch.display()
