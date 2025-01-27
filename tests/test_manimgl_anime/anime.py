from manimlib import *

sys.path.append("D://wroot//ManimGeo//src") # 使用绝对路径避免测试路径问题
from manimgeo.components import *
from manimgeo.utils.output import generate_simple_color
from manimgeo.anime.manimgl import GeoMapManager as GMM

class NinePointCircle(Scene):
    def construct(self):
        ## 进行几何构建

        # 构造三角形ABC
        A = FreePoint(np.array([-4, -2]), "A")
        B = FreePoint(np.array([3, -1]), "B")
        C = FreePoint(np.array([0, 3]), "C")
        
        # 构造中点
        AB_MID = MidPointPP(A, B, "AB_mid")
        BC_MID = MidPointPP(B, C, "BC_mid")
        AC_MID = MidPointPP(A, C, "AC_mid")
        
        # 构造边
        AB = LineSegmentPP(A, B, "AB")
        BC = LineSegmentPP(B, C, "BC")
        AC = LineSegmentPP(A, C, "AC")

        # 构造垂足
        AB_FOOT = VerticalPointPL(C, AB, "AB_foot")
        BC_FOOT = VerticalPointPL(A, BC, "BC_foot")
        AC_FOOT = VerticalPointPL(B, AC, "AC_foot")
        # 构造对应垂线
        AB_VERTICAL = LineSegmentPP(AB_FOOT, C, "AB_vertical")
        BC_VERTICAL = LineSegmentPP(BC_FOOT, A, "BC_vertical")
        AC_VERTICAL = LineSegmentPP(AC_FOOT, B, "AC_vertical")
        
        # 构造欧拉点
        ORTHOCENTER = IntersectionPointLL(
            InfinityLinePP(AB_FOOT, C),
            InfinityLinePP(BC_FOOT, A), 
            "Orthocenter"
        )

        # 构造中点对应线段
        EULER_A_LINE = LineSegmentPP(A, ORTHOCENTER, "A_orthocenter_line")
        EULER_B_LINE = LineSegmentPP(B, ORTHOCENTER, "B_orthocenter_line")
        EULER_C_LINE = LineSegmentPP(C, ORTHOCENTER, "C_orthocenter_line")
        # 构造中点
        EULER_A = MidPointL(EULER_A_LINE, "A_orthocenter_mid")
        EULER_B = MidPointL(EULER_B_LINE, "B_orthocenter_mid")
        EULER_C = MidPointL(EULER_C_LINE, "C_orthocenter_mid")
        
        # 构造九点圆
        NINE_POINT_CIRCLE = CirclePPP(AB_MID, BC_MID, AC_MID, "NinePointCircle")

        ## 进行动画构建
        gmm = GMM()

        def create_mobj(geos: List[BaseGeometry]) -> List[VMobject]:
            return [gmm.create_mobject_from_geometry(geo) for geo in geos]

        dot_a, dot_b, dot_c = create_mobj([A, B, C])
        l_ab, l_bc, l_ac = create_mobj([AB, BC, AC])
        ab_m, bc_m, ac_m = create_mobj([AB_MID, BC_MID, AC_MID])
        l_ab_v, l_bc_v, l_ac_v = create_mobj([AB_VERTICAL, BC_VERTICAL, AC_VERTICAL])
        ab_f, bc_f, ac_f = create_mobj([AB_FOOT, BC_FOOT, AC_FOOT])
        l_euler_a, l_euler_b, l_euler_c = create_mobj([EULER_A_LINE, EULER_B_LINE, EULER_C_LINE])
        euler_a, euler_b, euler_c = create_mobj([EULER_A, EULER_B, EULER_C])
        orth, npc = create_mobj([ORTHOCENTER, NINE_POINT_CIRCLE])

        def fit_color(*mobs: VMobject): 
            r, g, b = generate_simple_color()
            color = rgb_to_color((r / 255, g / 255, b / 255))

            for mob in mobs:
                if isinstance(mob, Dot):
                    mob.set_color(color)
                else:
                    mob.set_color(color)

        fit_color(dot_a, dot_b, dot_c)
        fit_color(l_ab, l_bc, l_ac)
        fit_color(ab_m, bc_m, ac_m)
        fit_color(l_ab_v, l_bc_v, l_ac_v)
        fit_color(ab_f, bc_f, ac_f)
        fit_color(orth)
        fit_color(l_euler_a, l_euler_b, l_euler_c)
        fit_color(euler_a, euler_b, euler_c)
        fit_color(npc)


        self.wait(1)
        self.play(Write(dot_a), Write(dot_b), Write(dot_c))
        self.wait(1)
        self.play(Write(l_ab), Write(l_bc), Write(l_ac))
        self.wait(1)
        self.play(Write(ab_m), Write(bc_m), Write(ac_m))
        self.wait(1)
        self.play(Write(l_ab_v), Write(l_bc_v), Write(l_ac_v))
        self.wait(1)
        self.play(Write(ab_f), Write(bc_f), Write(ac_f))
        self.wait(1)
        self.play(Write(orth))
        self.wait(1)
        self.play(Write(l_euler_a), Write(l_euler_b), Write(l_euler_c))
        self.wait(1)
        self.play(Write(euler_a), Write(euler_b), Write(euler_c))
        self.wait(1)
        self.play(Write(npc))
        self.wait(3)
