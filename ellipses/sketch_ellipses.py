import vsketch
import numpy as np
import math


class EllipsesSketch(vsketch.SketchClass):
    # Sketch parameters:
    count = vsketch.Param(25)
    twists = vsketch.Param(0.0, step=0.1, decimals=1)
    numsteps = vsketch.Param(15)
    sides = vsketch.Param(6)
    vradius = vsketch.Param(8)
    hradius = vsketch.Param(1)
    start_angle = vsketch.Param(0.0, 0.0, 1.0, step=0.005, decimals=3)
    easing_mode = vsketch.Param(
        "linear", choices=vsketch.EASING_FUNCTIONS.keys())
    easing_low_deadzone = vsketch.Param(0.0, 0.0, 100.0, step=5)
    easing_high_deadzone = vsketch.Param(0.0, 0.0, 100.0, step=5)
    easing_param = vsketch.Param(10.0, step=1.0, decimals=1)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=True)
        vsk.scale("cm")

        count = self.count
        numpoints = 500
        last = None

        # def xscale(step):
        #     return 1 + (count / 2) * step / count

        # def yscale(step):
        #     return 1 + (count / 2) * (count - step) / count

        def shape1(step, t):
            def xscale(step):
                #            return 1 + 8 * (count / 2 - abs(step - count / 2)) / count
                return self.hradius

            def yscale(step):
                #            return self.vradius * math.cos(self.twists * np.pi * abs(step - count / 2) / count)
                return self.vradius * math.cos(self.twists * np.pi * step / count)

            theta = (1 - t + self.start_angle) * 2 * np.pi
            return complex(
                xscale(step) * math.cos(theta) + step,
                yscale(step) * math.sin(theta)
            )

        def shape(step, t):
            wedge = 2 * np.pi / self.sides

            def xscale(step):
                #            return 1 + 8 * (count / 2 - abs(step - count / 2)) / count
                return self.hradius

            def yscale(step):
                #            return self.vradius * math.cos(self.twists * np.pi * abs(step - count / 2) / count)
                return self.vradius * math.cos(self.twists * np.pi * step / count)

            theta = (1 - t + self.start_angle) * 2 * np.pi
            length = 1
            alpha = (theta % wedge) - (wedge / 2)
            length = math.cos(wedge / 2) / math.cos(alpha)

            return complex(
                xscale(step) * length * math.cos(theta) + step,
                yscale(step) * length * math.sin(theta)
            )
            # return complex(
            #     xscale(step) * length * math.cos(theta) + 3 * (step % 8),
            #     yscale(step) * length * math.sin(theta) + (3 * step // 8)
            # )

        (steps, stepsize) = np.linspace(
            0, count, num=self.numsteps, retstep=True, endpoint=False)
        for (i, step) in enumerate(steps):
            points = [(t, shape(step, t), shape(step + stepsize, t))
                      for t in np.linspace(0, 1, num=numpoints)]

            lerped = [
                vsk.lerp(
                    p0,
                    p1,
                    vsk.easing(
                        t,
                        mode=self.easing_mode,
                        low_dead=self.easing_low_deadzone / 100.0,
                        high_dead=self.easing_high_deadzone / 100.0,
                        param=self.easing_param
                    )
                )
                for (t, p0, p1) in points
            ]
            if False:
                vsk.stroke(2)
                vsk.polygon([p0 for (_, p0, _) in points])
                if i == self.numsteps - 1:
                    vsk.polygon([p1 for (_, _, p1) in points])
            vsk.stroke(1)
            for p in lerped:
                if last:
                    vsk.line(last.real, last.imag, p.real, p.imag)
                last = p

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    EllipsesSketch.display()
