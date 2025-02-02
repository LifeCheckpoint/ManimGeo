import sys
from manimlib import *

sys.path.append("D://wroot//ManimGeo//src") # 使用绝对路径避免测试路径问题
from manimgeo.components import *
from manimgeo.anime.manimgl import GeoManimGLManager

class EulerLine(Scene):
    def construct(self):
        # 构造三角形ABC
        A = PointFree(np.array([-5, -1]), "A")
        B = PointFree(np.array([3, -2]), "B")
        C = PointFree(np.array([2, 3]), "C")
        AB = LineSegmentPP(A, B, "AB")
        BC = LineSegmentPP(B, C, "BC")
        AC = LineSegmentPP(A, C, "AC")

        # 重心 垂心 外心
        CENTROID = PointCentroidPPP(A, B, C, "Centroid")
        ORTHOCENTER = PointOrthocenterPPP(A, B, C, "Orthocenter")
        CIRCUMCENTER = PointCircumcenterPPP(A, B, C, "Circumcenter")

        # 创建几何动画管理器
        gmm = GeoManimGLManager()
        
        # 创建 ManimGL VMobject 图形
        dot_a, dot_b, dot_c = gmm.create_mobjects_from_geometry([A, B, C])
        l_ab, l_bc, l_ac = gmm.create_mobjects_from_geometry([AB, BC, AC])
        dot_ct, dot_orth, dot_cir = gmm.create_mobjects_from_geometry([CENTROID, ORTHOCENTER, CIRCUMCENTER])

        text_ct = Text("Centroid", font="Arial").move_to(dot_ct.get_center() + 0.2*(UP + RIGHT)).scale(0.3)
        text_orth = Text("Orthocenter", font="Arial").move_to(dot_orth.get_center() + 0.2*(UP + RIGHT)).scale(0.3)
        text_cir = Text("Circumcenter", font="Arial").move_to(dot_cir.get_center() + 0.2*(UP + RIGHT)).scale(0.3)

        # 设置颜色
        def fit_color(*mobs: VMobject, hex_color: str = "#FFFFFF"):
            color = rgb_to_color(hex_to_rgb(hex_color))
            [mob.set_color(color) for mob in mobs]       

        fit_color(dot_a, dot_b, dot_c, l_ab, l_bc, l_ac, hex_color="#F9F871")
        fit_color(dot_ct, text_ct, hex_color="#FF9671")
        fit_color(dot_orth, text_orth, hex_color="#FF6F91")
        fit_color(dot_cir, text_cir, hex_color="#845EC2")

        # 添加到场景演示
        self.wait(1)
        self.play(Write(dot_a), Write(dot_b), Write(dot_c))
        self.play(Write(l_ab), Write(l_bc), Write(l_ac))
        self.play(Write(dot_ct), Write(text_ct))
        self.play(Write(dot_orth), Write(text_orth))
        self.play(Write(dot_cir), Write(text_cir))
        self.wait(1)
        
        text_ct.add_updater(lambda m: m.move_to(dot_ct.get_center() + 0.2*(UP + RIGHT)))
        text_orth.add_updater(lambda m: m.move_to(dot_orth.get_center() + 0.2*(UP + RIGHT)))
        text_cir.add_updater(lambda m: m.move_to(dot_cir.get_center() + 0.2*(UP + RIGHT)))

        # 在几何管理器下执行约束动画变换
        with gmm:
            now = self.time
            dot_a.add_updater(lambda m: m.shift(0.01 * UP * math.sin((self.time - now)*2.5)))
            dot_b.add_updater(lambda m: m.shift(0.01 * RIGHT * math.cos((self.time - now)*2)))
            dot_c.add_updater(lambda m: m.shift(0.005 * (UP + LEFT) * math.sin((self.time - now)*1.5)))
            self.wait(20)

        [dot.clear_updaters() for dot in [dot_a, dot_b, dot_c]]
