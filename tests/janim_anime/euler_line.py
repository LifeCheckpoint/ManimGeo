import sys
from janim.imports import *

sys.path.append("D://wroot//ManimGeo//src") # 使用绝对路径避免测试路径问题
from manimgeo.components import *
from manimgeo.anime.janim import GeoJAnimManager

class EulerLine(Timeline):
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
        gjm = GeoJAnimManager()
        
        dot_a, dot_b, dot_c = gjm.create_vitems_with_add_updater([A, B, C], 20, self)
        l_ab, l_bc, l_ac = gjm.create_vitems_with_add_updater([AB, BC, AC], 20, self)
        dot_ct, dot_orth, dot_cir = gjm.create_vitems_with_add_updater([CENTROID, ORTHOCENTER, CIRCUMCENTER], 20, self)

        def text_updater(dot: Dot, text: str):
            coord = dot.current().points.box.center + 0.2 * (UP + RIGHT)
            text_vitem = Text(text, font="Arial")
            text_vitem.fill.set("#845EC2")
            text_vitem.points.move_to(coord).scale(0.5)
            return text_vitem

        # 设置颜色
        def fit_color(*mobs: VItem, hex_color: str = "#FFFFFF"):
            for mob in mobs:
                mob.stroke.set(hex_color)
                mob.fill.set(hex_color)

        fit_color(dot_a, dot_b, dot_c, l_ab, l_bc, l_ac, hex_color="#F9F871")
        fit_color(dot_cir, dot_orth, dot_ct, hex_color="#845EC2")

        # 添加到场景演示
        self.forward()
        self.play(Write(dot_a), Write(dot_b), Write(dot_c))
        self.play(Write(l_ab), Write(l_bc), Write(l_ac))
        self.play(Write(dot_ct))
        self.play(Write(dot_orth))
        self.play(Write(dot_cir))
        self.prepare(
            ItemUpdater(None, lambda _: text_updater(dot_ct, "Centroid")),
            ItemUpdater(None, lambda _: text_updater(dot_orth, "Orthocenter")),
            ItemUpdater(None, lambda _: text_updater(dot_cir, "Circumcenter")),
            duration=15
        )
        self.forward()

        self.play(
            DataUpdater(dot_a, lambda data, p: data.points.shift(UP * math.sin(p.alpha*2.5))),
            DataUpdater(dot_b, lambda data, p: data.points.shift(RIGHT * math.sin(p.alpha*2))),
            DataUpdater(dot_c, lambda data, p: data.points.shift((UP + LEFT) * math.sin(p.alpha*1.5))),
            duration=10
        )