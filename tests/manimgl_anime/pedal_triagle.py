import sys
from manimlib import *

sys.path.append("D://wroot//ManimGeo//src") # 使用绝对路径避免测试路径问题
from manimgeo.components import *
from manimgeo.anime.manimgl import GeoManimGLManager

class PedalIteration(Scene):
    def pedal_triangle_iteration(self, gmm: GeoManimGLManager, base_points: list[Point], iterations: int) -> List[Dot]:
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
                PointVerticalPL(current_points[0], lines_inf[1], f"P{i}_A"),
                PointVerticalPL(current_points[1], lines_inf[2], f"P{i}_B"),
                PointVerticalPL(current_points[2], lines_inf[0], f"P{i}_C")
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
        A = PointFree(np.array([-4, -3]), "A")
        B = PointFree(np.array([3, -2]), "B")
        C = PointFree(np.array([0, 3.5]), "C")
        
        gmm = GeoManimGLManager()

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
            GeoUtils.geo_print_dependencies(A)