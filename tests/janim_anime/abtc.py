# Ref from https://zhuanlan.zhihu.com/p/670419123

import sys
from janim.imports import *

sys.path.append("D://wroot//ManimGeo//src") # 使用绝对路径避免测试路径问题
from manimgeo.components import *
from manimgeo.anime.janim import GeoJAnimManager

class ABTC(Timeline):
    def construct(self):
        def fit_color(*mobs_or_color):
            mobs = []
            for item in mobs_or_color:
                if isinstance(item, VItem):
                    mobs.append(item)
                else:
                    for mob in mobs:
                        mob.stroke.set(item)
                        mob.fill.set(item)
                    mobs = []
        def get_text(text: str, shift: np.ndarray = ORIGIN):
            t = Text(text, format=Text.Format.RichText, font=["Arial", "Microsoft YaHei"])
            t.points.scale(0.9).align_to(LEFT * 6.5, LEFT).align_to(UP * 3.5, UP)
            t.points.shift(shift)
            return t

        gjm = GeoJAnimManager()

        t_title = get_text("ASK: 作一个圆，使其过两已知点 <c RED>A</c> <c BLUE>B</c>，并且与一已知圆 <c YELLOW>O</c> 相切")
        t_step_1 = get_text("以 <c RED>A</c> 为反演中心，任意长为半径，建立圆 <c RED>A</c>")
        t_step_2 = get_text("作 <c BLUE>B</c> 及圆周 <c YELLOW>C</c> 反演点 <c BLUE>B'</c> 以及反演圆 <c YELLOW>C'<c BLUE>", DOWN * 0.5)
        t_step_3 = get_text("过 <c BLUE>B'</c> 作 <c YELLOW>C'</c> 的两条切线")
        t_step_4 = get_text("再作两切线关于圆 A 的反演圆", DOWN * 0.5)
        t_step_5 = get_text("隐藏辅助线即为所得")
        
        A = PointFree(np.array([1.3, 1.3]), "A")
        B = PointFree(np.array([1.8, -0.8]))
        C = PointFree(np.array([-2.5, 0]), "C")
        CIRCLE_C = CirclePR(C, 1.6, "Circle C")
        INV_A_CIRCLE = CirclePR(A, 1.5, "Inverse Circle A")
        INV_B = PointInversionPCir(B, INV_A_CIRCLE, "B'")
        INV_C_CIRCLE = CircleInverseCirCir(CIRCLE_C, INV_A_CIRCLE, "Inverse Circle C'")
        TANGENTS_INV_B = LineOfLines2List(Lines2TangentsCirP(INV_C_CIRCLE, INV_B, "Tangents Through B' Of C'"))
        INTERSECTIONS_INVA_TANB_0 = PointOfPoints2List(Points2IntersectionLCir(TANGENTS_INV_B[0], INV_A_CIRCLE))
        INTERSECTIONS_INVA_TANB_1 = PointOfPoints2List(Points2IntersectionLCir(TANGENTS_INV_B[1], INV_A_CIRCLE))
        INVERSE_TAN_0 = CirclePPP(INTERSECTIONS_INVA_TANB_0[0], INTERSECTIONS_INVA_TANB_0[1], A, "Inverse Circle Of Tangent 0")
        INVERSE_TAN_1 = CirclePPP(INTERSECTIONS_INVA_TANB_1[0], INTERSECTIONS_INVA_TANB_1[1], A, "Inverse Circle Of Tangent 1")

        GeoUtils.print_dependencies(A)

        dot_a, dot_b, dot_c, circle_c = gjm.create_vitems_with_add_updater([A, B, C, CIRCLE_C], self, 50)
        inv_a, inv_b, inv_c = gjm.create_vitems_with_add_updater([INV_A_CIRCLE, INV_B, INV_C_CIRCLE], self, 50)
        t_inv_b0, t_inv_b1, inv_tan0, inv_tan1 = gjm.create_vitems_with_add_updater([TANGENTS_INV_B[0], TANGENTS_INV_B[1], INVERSE_TAN_0, INVERSE_TAN_1], self, 50)

        fit_color(dot_a, inv_a, RED, dot_b, inv_b, BLUE, dot_c, circle_c, inv_c, YELLOW, t_inv_b0, t_inv_b1, PURPLE_B, inv_tan0, inv_tan1, PURPLE_E)

        def playEx(comps: List):
            for comp in comps:
                if isinstance(comp, Number):
                    self.forward(comp)
                elif isinstance(comp, VItem):
                    self.play(Write(comp))
                elif isinstance(comp, list):
                    self.play(*[Write(c) for c in comp])
                elif isinstance(comp, tuple):
                    self.play(*[FadeOut(c) for c in comp])

        playEx([1, t_title, 1, [dot_a, dot_b, dot_c], 1, circle_c, 3, (t_title, ), t_step_1, t_step_2, 1, inv_a])
        self.play(Transform(dot_b, inv_b, hide_src=False))
        self.play(Transform(circle_c, inv_c, hide_src=False))
        playEx([
            3, (t_step_1, t_step_2), t_step_3, t_step_4, 1, t_inv_b0, t_inv_b1, 1, inv_tan0, inv_tan1, 3, (t_step_3, t_step_4),
            t_step_5, 1, (inv_a, inv_b, inv_c), (t_inv_b0, t_inv_b1), 2
        ])
        playEx([[inv_a, inv_b, inv_c, t_inv_b0, t_inv_b1]])
        self.play(
            dot_a.anim.points.move_to(1.8 * UP + 2.8 * RIGHT),
            dot_b.anim.points.move_to(-1 * UP + -2 * RIGHT),
            dot_c.anim.points.move_to(1 * UP + -0.8 * RIGHT),
            duration=5
        )
        playEx([(inv_a, inv_b, inv_c, t_inv_b0, t_inv_b1)])
        self.forward(3)