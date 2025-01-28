from manimlib import *

sys.path.append("D://wroot//ManimGeo//src") # 使用绝对路径避免测试路径问题
from manimgeo.components import *
from manimgeo.anime.manimgl import GeoManimGLMap

class EulerLine(Scene):
    def construct(self):
        # 构造三角形ABC
        A = FreePoint(np.array([-5, -1]), "A")
        B = FreePoint(np.array([3, -2]), "B")
        C = FreePoint(np.array([2, 3]), "C")
        AB = LineSegmentPP(A, B, "AB")
        BC = LineSegmentPP(B, C, "BC")
        AC = LineSegmentPP(A, C, "AC")

        # 重心 垂心 外心
        CENTROID, _ = CentroidPPP(A, B, C, "Centroid")
        ORTHOCENTER, _ = OrthocenterPPP(A, B, C, "Orthocenter")
        CIRCUMCENTER, _ = CircumcenterPPP(A, B, C, "Circumcenter")

        # 创建几何动画管理器
        gmm = GeoManimGLMap()
        
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

class NinePointCircle(Scene):
    def construct(self):
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
        
        # 构造垂点
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

        # 创建几何动画管理器
        gmm = GeoManimGLMap()

        # 手动创建 ManimGL VMobject 图形
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

        # 美化
        def fit_color(*mobs: VMobject, hex_color: str = "#FFFFFF"):
            color = rgb_to_color(hex_to_rgb(hex_color))
            [mob.set_color(color) for mob in mobs]

        fit_color(dot_a, dot_b, dot_c, hex_color="#845EC2")
        fit_color(l_ab, l_bc, l_ac, hex_color="#845EC2")
        fit_color(ab_m, bc_m, ac_m, hex_color="#FF6F91")
        fit_color(l_ab_v, l_bc_v, l_ac_v, hex_color="#FF9671")
        fit_color(ab_f, bc_f, ac_f, hex_color="#FF9671")
        fit_color(orth, hex_color="#FF9671")
        fit_color(l_euler_a, l_euler_b, l_euler_c, hex_color="#D65DB1")
        fit_color(euler_a, euler_b, euler_c, hex_color="#F9F871")
        fit_color(npc, hex_color="#F9F871")
        
        # 添加到场景演示
        self.wait(1)
        self.play(Write(dot_a), Write(dot_b), Write(dot_c))
        self.play(Write(l_ab), Write(l_bc), Write(l_ac))
        self.play(Write(ab_m), Write(bc_m), Write(ac_m))
        self.play(Write(l_ab_v), Write(l_bc_v), Write(l_ac_v))
        self.play(Write(ab_f), Write(bc_f), Write(ac_f))
        self.play(Write(orth))
        self.play(Write(l_euler_a), Write(l_euler_b), Write(l_euler_c))
        self.play(Write(euler_a), Write(euler_b), Write(euler_c))
        self.play(Write(npc))
        self.wait(2)

        # 在几何管理器下执行约束动画变换
        with gmm:
            self.play(dot_a.animate.shift(RIGHT*4 + UP * 2), run_time=5, rate_func=smooth)
            self.wait(1)
            self.play(dot_b.animate.shift(RIGHT*0.5 + DOWN * 2), run_time=5, rate_func=smooth)
            self.wait(2)

class PedalIteration(Scene):
    def pedal_triangle_iteration(self, gmm: GeoManimGLMap, base_points: list[PointLike], iterations: int) -> List[Dot]:
        """垂足三角形迭代动画生成"""
        colors = ["#F9F871", "#FF9671", "#FF6F91", "#845EC2"]  # 颜色循环
        
        current_points = base_points.copy()
        for i in range(iterations + 1):
            # 三角形边
            lines_inf = [
                InfinityLinePP(current_points[0], current_points[1], f"L{i}_AB"),
                InfinityLinePP(current_points[1], current_points[2], f"L{i}_BC"),
                InfinityLinePP(current_points[2], current_points[0], f"L{i}_CA")
            ]
            line_seg = [
                LineSegmentPP(current_points[0], current_points[1], f"Ls{i}_AB"),
                LineSegmentPP(current_points[1], current_points[2], f"Ls{i}_BC"),
                LineSegmentPP(current_points[2], current_points[0], f"Ls{i}_CA")
            ]
            
            # 生成当前层的几何图形
            mob_points = gmm.create_mobjects_from_geometry(current_points)
            mob_lines_inf = gmm.create_mobjects_from_geometry(lines_inf)
            mob_lines_seg = gmm.create_mobjects_from_geometry(line_seg)

            if i == 0:
                top_mob_points = mob_points
            
            # 显示构建过程
            color = colors[i % len(colors)]
            anime = lambda Op, mobs: self.play(
                *[Op(mob) for mob in mobs],
                run_time=1,
                rate_func=smooth
            )

            anime(Write, mob_lines_inf)
            anime(Write, mob_points)
            anime(FadeOut, mob_lines_inf)
            anime(Write, mob_lines_seg)
            self.play(
                *[mob.animate.set_color(color) for mob in mob_points + mob_lines_seg],
                run_time=0.5,
                rate_func=smooth
            )
            
            # 最后一次迭代不需要生成下一层
            if i == iterations:
                break
                
            # 计算下一层垂足点
            new_points = [
                VerticalPointPL(current_points[0], lines_inf[1], f"P{i}_A"),
                VerticalPointPL(current_points[1], lines_inf[2], f"P{i}_B"),
                VerticalPointPL(current_points[2], lines_inf[0], f"P{i}_C")
            ]

            # 三角形垂线
            lines_ver = [
                LineSegmentPP(current_points[0], new_points[0], f"ver_0"),
                LineSegmentPP(current_points[1], new_points[1], f"ver_1"),
                LineSegmentPP(current_points[2], new_points[2], f"ver_2")
            ]

            mobj_lines_ver = gmm.create_mobjects_from_geometry(lines_ver)
            anime(Write, mobj_lines_ver)
            anime(FadeOut, mobj_lines_ver)

            current_points = new_points

        return top_mob_points

    def construct(self):
        # 初始化自由点
        A = FreePoint(np.array([-4, -3]), "A")
        B = FreePoint(np.array([3, -2]), "B")
        C = FreePoint(np.array([0, 3.5]), "C")
        
        gmm = GeoManimGLMap()

        # 迭代构建
        dot_a, dot_b, dot_c = self.pedal_triangle_iteration(gmm, [A, B, C], iterations=4)
        
        with gmm:
            self.wait(1)
            dot_a.add_updater(lambda m: m.shift(0.03*UP*math.sin(self.time)))
            dot_b.add_updater(lambda m: m.shift(0.03*RIGHT*math.cos(self.time)))
            dot_c.add_updater(lambda m: m.shift(0.03*LEFT*math.sin(2*self.time)))
            self.wait(8)
            
            # 清除跟踪器以停止移动点对
            [dot.clear_updaters() for dot in [dot_a, dot_b, dot_c]]

            # ManimGEO 通过跟踪器获取点的坐标
            # 因此清除所有跟踪器后要重新添加叶子节点的跟踪器关联
            [gmm.register_updater(obj, mobj) for obj, mobj in [(A, dot_a), (B, dot_b), (C, dot_c)]]
            
            def param_run(t: float, sclae: float) -> np.ndarray:
                AA, BB, CC = 1, 1.5, 0.5
                DD, EE, FF = 1, 1, 0.7
                omega_1, omega_2, omega_3 = 1, 2, 3

                T = t * sclae
                x = AA * np.cos(omega_1 * T) + BB * np.sin(omega_2 * T) + CC * np.cos(omega_3 * T)
                y = DD * np.sin(omega_1 * T) + EE * np.cos(omega_2 * T) + FF * np.sin(omega_3 * T)
                return 0.03*(1 / t**0.5)*np.array([x, y, 0])

            dot_a.add_updater(lambda m: m.shift(param_run(self.time, 1)))
            dot_b.add_updater(lambda m: m.shift(param_run(self.time, 1.5)))
            dot_c.add_updater(lambda m: m.shift(param_run(self.time, 2)))
            self.wait(15)

            # 清除跟踪器以停止动画
            [dot.clear_updaters() for dot in [dot_a, dot_b, dot_c]]
            self.wait(2)

            # 输出 A 的依赖关系
            geo_print_dependencies(A)