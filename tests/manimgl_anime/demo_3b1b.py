import sys
from manimlib import *

sys.path.append("D://wroot//ManimGeo//src") # 使用绝对路径避免测试路径问题
from manimgeo.components import *
from manimgeo.anime.manimgl import GeoManimGLManager

class Demo3B1B(Scene):
    def construct(self):
        P1 = PointFree(np.array([-2.5, -0.5]), "P1")
        P2 = PointFree(np.array([1.5, 1]), "P2")
        P3 = PointFree(np.array([4, -1]), "P3")
        CIR1 = CirclePR(P1, 0.3, "Cir1")
        CIR2 = CirclePR(P2, 2.1, "Cir2")
        CIR3 = CirclePR(P3, 1.0, "Cir3")
        L12_0, L12_1 = LineOfLines2List(Lines2TangentsOutCirCir(CIR1, CIR2, "t12"))
        L23_0, L23_1 = LineOfLines2List(Lines2TangentsOutCirCir(CIR2, CIR3, "t23"))
        L31_0, L31_1 = LineOfLines2List(Lines2TangentsOutCirCir(CIR3, CIR1, "t31"))
        S1 = PointIntersectionLL(L12_0, L12_1, name="S1")
        S2 = PointIntersectionLL(L23_0, L23_1, name="S2")
        S3 = PointIntersectionLL(L31_0, L31_1, name="S3")
        L_TANGENT = InfinityLinePP(S1, S2) # S1 S2 S3

        gmm = GeoManimGLManager()

        p1, p2, p3 = gmm.create_mobjects_from_geometry([P1, P2, P3])
        cir1, cir2, cir3 = gmm.create_mobjects_from_geometry([CIR1, CIR2, CIR3])
        l12_0, l12_1, l23_0, l23_1, l31_0, l31_1 = gmm.create_mobjects_from_geometry([L12_0, L12_1, L23_0, L23_1, L31_0, L31_1])
        s1, s2, s3, l_tangent = gmm.create_mobjects_from_geometry([S1, S2, S3, L_TANGENT])
        l_group = VGroup(l12_0, l12_1, l23_0, l23_1, l31_0, l31_1)

        def fit_color(*mobs: VMobject, hex_color: str = "#FFFFFF"):
            color = rgb_to_color(hex_to_rgb(hex_color))
            [mob.set_color(color) for mob in mobs]       

        fit_color(p1, cir1, l12_0, l12_1, s1, hex_color="#F9F871")
        fit_color(p2, cir2, l31_0, l31_1, s2, hex_color="#FF9671")
        fit_color(p3, cir3, l23_0, l23_1, s3, hex_color="#FF6F91")
        fit_color(l_tangent, hex_color="#845EC2")
        
        self.wait(1)
        self.play(Write(p1), Write(p2), Write(p3))
        self.play(Write(cir1), Write(cir2), Write(cir3))
        self.wait(1)
        self.play(Write(s1))
        self.play(Write(l12_0), Write(l12_1))
        self.play(Write(s2))
        self.play(Write(l23_0), Write(l23_1))
        self.play(Write(s3))
        self.play(Write(l31_0), Write(l31_1))
        self.wait(1)
        self.play(Write(l_tangent))
        self.wait(1)
        self.play(FadeOut(l_group))
        self.wait(1)

        with gmm:
            self.play(
                p1.animate.move_to(np.array([1.5, 2, 0])),
                p2.animate.move_to(np.array([4, -1, 0])),
                p3.animate.move_to(np.array([-1.5, -0.5, 0])),
                run_time=5,
                rate_func=smooth
            )
        