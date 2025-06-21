# ManimGeo - 几何动画辅助库

ManimGeo 是一个用于简化几何图形创建和动画生成的辅助库。它提供丰富的几何元素和操作，帮助快速构建复杂的几何场景。

*目前开发中，单元测试尚未完成，欢迎 PR！*

## 主要特性

- **几何元素创建**：支持点、线、圆、角等基本几何元素的创建
- **几何关系处理**：自动处理中点、垂足、交点等几何关系
- **几何变换**：支持反演等几何变换操作
- **依赖管理**：自动维护几何元素间的依赖关系
- **动画集成**：与 Manim 等动画系统的高集成

## 项目文档

[ManimGeo 文档](https://manimgeo.readthedocs.io/zh-cn/latest/)

## 安装 ManimGeo

```bash
# 仅安装数值计算
pip install manimgeo

# 安装 manimgl 集成
pip install manimgeo[manim]

# 安装 janim 集成
pip install manimgeo[janim]

# 全部安装
pip install manimgeo[full]
```

或使用 uv 进行安装（推荐）

```bash
uv add manimgeo[full]
```

## 样例展示

https://github.com/user-attachments/assets/36fec8c6-ad72-4b34-b9fc-f636a6808cfb

https://github.com/user-attachments/assets/b47f8a04-351a-42b2-8f1a-f4bcf2d0d79f

https://github.com/user-attachments/assets/e94ea012-1053-4585-82dd-058d04feb9ac
