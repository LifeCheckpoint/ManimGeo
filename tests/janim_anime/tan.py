from janim.imports import *

class UpdaterExample(Timeline):
    def construct(self):
        square = Square(fill_color=BLUE_E, fill_alpha=1).show()
        brace = Brace(square, UP).show()

        def text_updater(p: UpdaterParams):
            cmpt = brace.current().points
            return cmpt.create_text(f'Width = {cmpt.brace_length:.2f}')

        self.prepare(
            DataUpdater(
                brace,
                lambda data, p: data.points.match(square.current())
            ),
            ItemUpdater(None, text_updater),
            duration=10
        )
        self.forward()
        self.play(square.anim.points.scale(2))
        self.play(square.anim.points.scale(0.5))
        self.play(square.anim.points.set_width(5, stretch=True))

        w0 = square.points.box.width

        self.play(
            DataUpdater(
                square,
                lambda data, p: data.points.set_width(
                    w0 + 0.5 * w0 * math.sin(p.alpha * p.range.duration)
                )
            ),
            duration=5
        )
        self.forward()