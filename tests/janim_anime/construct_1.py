# Ref from https://www.zhihu.com/question/9088356148

from janim.imports import *
from typing import Tuple, List
from manimgeo.components import *
from manimgeo.anime.janim import GeoJAnimManager

class CON1(Timeline):
    def construct(self):
        def fit_color(*item_color: Tuple[List[VItem], any]):
            for items, color in item_color:
                for item in items:
                    item.stroke.set(color)
                    item.fill.set(color)
        def get_text(text: str, shift: np.ndarray = ORIGIN):
            t = Text(text, format=Text.Format.RichText, font=["Arial", "Microsoft YaHei"])
            t.points.scale(0.9).align_to(LEFT * 6.5, LEFT).align_to(UP * 3.5, UP)
            t.points.shift(shift)
            return t
        def label(*objs: Point, position: np.ndarray = (UP + RIGHT) * 0.2):
            texts = []
            for obj in objs:
                t = Text(obj.name, format=Text.Format.RichText, font=["Arial", "Microsoft YaHei"])
                t.points.scale(0.6).move_to(np.append(obj.coord, 0) + position)
                texts.append(t)
            return texts

        gjm = GeoJAnimManager(self)
        GeoUtils.set_debug(False)

        A = PointFree(np.array([-3.5, -1.2]), "A")
        B = PointFree(np.array([0.6, 3.3]), "B")
        C = PointFree(np.array([3.5, -1.2]), "C")
        AB = LineSegmentPP(A, B, "AB")
        BC = LineSegmentPP(B, C, "BC")
        CA = LineSegmentPP(C, A, "CA")
        I = PointIncenterPPP(A, B, C, "I")
        AI = LineSegmentPP(A, I, "AI")
        CI = LineSegmentPP(C, I, "CI")
        L = PointMidL(AI, "L")
        M = PointMidL(CA, "M")
        N = PointMidL(CI, "N")
        D = PointIntersectionLCir(CA, CircleL(BC), lambda p: not np.allclose(p, C.coord, atol=1e-3), True, "D")
        BD = LineSegmentPP(B, D, "BD")
        CIRCLE_IN_ABD = CircleInscribePPP(A, B, D)
        E = PointIntersectionLCir(CA, CIRCLE_IN_ABD, None, True, "E")[0]
        F = PointIntersectionLCir(BD, CIRCLE_IN_ABD, None, True, "F")[0]
        J = PointCircumcenterPPP(A, I, C, "J")
        CIRCLE_J = CirclePPP(A, I, C, "Circle J")
        CIRCLE_OMEGA = CirclePPP(J, M, D, "Circle Omega")
        NM = RayPP(N, M, "NM")
        JL = LineSegmentPP(J, L, "JL")
        P = PointIntersectionLCir(NM, CIRCLE_OMEGA, lambda p: not np.allclose(p, M.coord, atol=1e-3), True, "P")
        Q = PointIntersectionLCir(JL, CIRCLE_OMEGA, lambda p: not np.allclose(p, J.coord, atol=1e-3), True, "Q")
        PQ = InfinityLinePP(P, Q, "PQ")
        EF = InfinityLinePP(E, F, "EF")
        RES = PointIntersectionLL(PQ, EF, name="Result")

        def create(*objs):
            return gjm.create_vitems_with_add_updater(objs, 100)

        dot_a, dot_b, dot_c = create(A, B, C)
        line_ab, line_bc, line_ca = create(AB, BC, CA)
        dot_i, line_ai, line_ci = create(I, AI, CI)
        dot_l, dot_m, dot_n = create(L, M, N)
        dot_d, line_bd = create(D, BD)
        circle_abd, dot_e, dot_f = create(CIRCLE_IN_ABD, E, F)
        dot_j, circle_j, circle_omega = create(J, CIRCLE_J, CIRCLE_OMEGA)
        line_nm, line_jl = create(NM, JL)
        dot_p, dot_q = create(P, Q)
        line_pq, line_ef = create(PQ, EF)
        res_dot = create(RES)[0]

        for dot in [dot_a, dot_b, dot_c, dot_i, dot_l, dot_m, dot_n, dot_d, dot_e, dot_f, dot_j, dot_p, dot_q, res_dot]:
            dot.points.scale(0.5)

        La, Lb, Lc, Li, Ll, Lm, Ln, Ld, Le, Lf, Lj, Lp, Lq = label(A, B, C, I, L, M, N, D, E, F, J, P, Q)

        fit_color(
            ([dot_a, dot_b, dot_c, line_ab, line_bc, line_ca, La, Lb, Lc], "#C6FFDD"),
            ([dot_i, line_ai, line_ci, Li], "#EAE4A3"),
            ([dot_l, dot_m, dot_n, dot_d, line_bd, Ll, Lm, Ln, Ld], "#FBD786"),
            ([circle_abd, dot_e, dot_f, Le, Lf], "#FAC884"),
            ([dot_j, circle_j, circle_omega, line_nm, line_jl, Lj], "#F89B80"),
            ([dot_p, dot_q, Lp, Lq], "#F8857F"),
            ([line_pq, line_ef, res_dot], "#F7797D")
        )

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
                elif isinstance(comp, set):
                    self.play(*comp)

        t1 = get_text("如图，在三角形 <c #C6FFDD>ABC</c> 中")
        t2 = get_text("<c #EAE4A3>I</c> 为三角形 <c #C6FFDD>ABC</c> 的内心")
        t3 = get_text("连接 <c #EAE4A3>IA</c> 与 <c #EAE4A3>IC</c>")
        t4 = get_text("作出 <c #EAE4A3>IA</c> <c #EAE4A3>IC</c> 与 <c #C6FFDD>AC</c> 的中点")
        t5 = get_text("在线段 <c #C6FFDD>AC</c> 上找一点 <c #FBD786>D</c>，满足 <c #C6FFDD>BC</c>=<c #FBD786>BD</c>")
        t6 = get_text("作三角形 <c #C6FFDD>AB</c><c #FBD786>D</c> 的内接圆")
        t7 = get_text("内接圆与 <c #C6FFDD>A</c><c #FBD786>D</c> 切于 <c #FAC884>E</c>，与 <c #C6FFDD>B</c><c #FBD786>D</c> 切于 <c #FAC884>F</c>")
        t8 = get_text("作出三角形 <c #EAE4A3>AIC</c> 的外心 <c #F89B80>J</c>")
        t9 = get_text("作出三角形 <c #F89B80>J</c><c #FBD786>MD</c> 的外接圆 <c #F89B80>ω</c>")
        t10 = get_text("连接 <c #F89B80>MN</c> 与  <c #F89B80>JL</c>，与 <c #F89B80>ω</c> 交于点 <c #F8857F>P Q</c>")
        t11 = get_text("<fs 1.2>求证：</fs><c #F8857F>PQ</c>，<c #F89B80>L</c><c #FBD786>N</c>，<c #F7797D>EF</c> 三线共点")

        playEx([
            1, t1, 1, [dot_a, dot_b, dot_c], [La, Lb, Lc], 1, [line_ab, line_bc, line_ca], 2,
            (t1,), t2, 1, dot_i, Li, 3,
            (t2,), t3, 1, line_ai, line_ci, 2,
            (t3,), t4, 1, [dot_l, dot_m, dot_n], [Ll, Lm, Ln], 2,
            (t4,), t5, 1, dot_d, Ld, 1, {Transform(line_bc, line_bd, hide_src=False)}, 2,
            (t5,), t6, 1, circle_abd, 2, 
            (t6,), t7, 1, [dot_e, dot_f], [Le, Lf], 3,
            (t7,), t8, 1, circle_j, 1, dot_j, (circle_j,), Lj, 2,
            (t8,), t9, 1, circle_omega, 2,
            (t9,), t10, 1, [line_nm, line_jl], 2, [dot_p, dot_q], [Lp, Lq], 2,
            (t10,), t11, 1, [line_pq, line_ef], 1, res_dot, 1, (line_pq, line_ef), 10
        ])