# Ref from https://www.zhihu.com/question/9088356148

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

        A = PointFree(np.array([-4, -2]), "A")
        B = PointFree(np.array([0.6, 2]), "B")
        C = PointFree(np.array([4, -2]), "C")
        AB = LineSegmentPP(A, B, "AB")
        BC = LineSegmentPP(B, C, "BC")
        CA = LineSegmentPP(C, A, "CA")
        I = PointIncenterPPP(A, B, C, "I")
        AI = LineSegmentPP(A, I, "AI")
        CI = LineSegmentPP(C, I, "CI")
        L = PointMidL(AI, "L")
        M = PointMidL(CA, "M")
        N = PointMidL(CI, "N")
        D_AND_C = PointOfPoints2List(Points2IntersectionLCir(CA, CircleL(BC), True, "D And C"))
        D = D_AND_C[0] if np.allclose(D_AND_C[1].coord, C.coord) else D_AND_C[1]
        BD = LineSegmentPP(B, D, "BD")
        CIRCLE_IN_ABD = CircleInscribePPP(A, B, D)
        E = PointOfPoints2List(Points2IntersectionLCir(CA, CIRCLE_IN_ABD, True, "Int E"))[0]
        F = PointOfPoints2List(Points2IntersectionLCir(BD, CIRCLE_IN_ABD, True, "Int F"))[0]
        J = PointCircumcenterPPP(A, I, C, "J")
        CIRCLE_OMEGA = CirclePPP(J, M, D, "Circle Omega")
        NM = RayPP(N, M, "NM")
        JL = LineSegmentPP(J, L, "JL")
        M_AND_P = PointOfPoints2List(Points2IntersectionLCir(NM, CIRCLE_OMEGA, True))
        Q_AND_J = PointOfPoints2List(Points2IntersectionLCir(JL, CIRCLE_OMEGA, True))
        P = M_AND_P[0] if np.allclose(M_AND_P[1].coord, M.coord) else M_AND_P[1]
        Q = Q_AND_J[0] if np.allclose(Q_AND_J[1].coord, J.coord) else Q_AND_J[1]
        PQ = InfinityLinePP(P, Q, "PQ")
        EF = InfinityLinePP(E, F, "EF")
        RES = PointIntersectionLL(PQ, EF, name="Result")

        # 创建所有几何对象的可视项并绑定颜色
        dot_a, dot_b, dot_c = gjm.create_vitems_with_add_updater([A, B, C], self, 50)
        line_ab, line_bc, line_ca = gjm.create_vitems_with_add_updater([AB, BC, CA], self, 50)
        dot_i, line_ai, line_ci = gjm.create_vitems_with_add_updater([I, AI, CI], self, 50)
        dot_l, dot_m, dot_n = gjm.create_vitems_with_add_updater([L, M, N], self, 50)
        dot_d, line_bd = gjm.create_vitems_with_add_updater([D, BD], self, 50)
        circle_abd, dot_e, dot_f = gjm.create_vitems_with_add_updater([CIRCLE_IN_ABD, E, F], self, 50)
        dot_j, circle_omega = gjm.create_vitems_with_add_updater([J, CIRCLE_OMEGA], self, 50)
        line_nm, line_jl = gjm.create_vitems_with_add_updater([NM, JL], self, 50)
        dot_p, dot_q = gjm.create_vitems_with_add_updater([P, Q], self, 50)
        line_pq, line_ef = gjm.create_vitems_with_add_updater([PQ, EF], self, 50)
        res_dot = gjm.create_vitems_with_add_updater([RES], self, 50)[0]

        # 配置颜色方案
        fit_color(
            dot_a, RED, dot_b, GREEN, dot_c, BLUE,  # 基础三角形顶点
            line_ab, line_bc, line_ca, GREY_A,      # 边线
            dot_i, line_ai, line_ci, PURPLE_D,      # 内心及相关线段
            dot_l, dot_m, dot_n, ORANGE,            # 中点集合
            dot_d, line_bd, TEAL_D,                 # 交点D及线段BD
            circle_abd, dot_e, dot_f, PINK,         # 内切圆及相关点
            dot_j, circle_omega, GOLD_D,            # 外心及圆Omega
            line_nm, line_jl, MAROON_D,             # 构造射线
            dot_p, dot_q, YELLOW_D,                 # 圆交点
            line_pq, line_ef, "#00FFFF",            # 无限直线
            res_dot, "#FF00FF"                      # 最终结果点
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

        # 分阶段动画演示
        playEx([
            1, [dot_a, dot_b, dot_c], 2,           # 显示ABC三点
            [line_ab, line_bc, line_ca], 3,        # 绘制三角形边
            [dot_i, line_ai, line_ci], 2,          # 显示内心及相关线段
            [dot_l, dot_m, dot_n], 1.5,            # 显示中点L/M/N
            [dot_d, line_bd], 2,                   # 显示交点D及BD线段
            [circle_abd, dot_e, dot_f], 3,         # 内切圆及交点E/F
            [dot_j, circle_omega], 2,              # 外心J及圆Omega
            [line_nm, line_jl], 1.5,               # 显示构造射线NM/JL
            [dot_p, dot_q], 2,                     # 显示圆交点P/Q
            [line_pq, line_ef], 3,                 # 绘制无限直线PQ/EF
            [res_dot], 4,                          # 高亮显示结果点
            (circle_abd, line_nm, line_jl), 2      # 淡化辅助元素
        ])

        playEx([[dot_a, dot_b, dot_c, line_ab, line_bc, line_ca], 2])

        # # 最终聚焦结果
        # self.play(
        #     res_dot.anim.points.scale(3).set_color("#FF0000"),
        #     rate_func=there_and_back,
        #     duration=3
        # )
        self.forward(20)