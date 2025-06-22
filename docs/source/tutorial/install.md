# 安装

ℹ `manimgeo` 库要求的最低 python 版本是 `3.10`，如果要使用其 `JAnim` 等集成，则要求最低版本是 `3.12`

---

## 安装 Python

访问官方网站以下载 Python 👉 [Python Download](https://www.python.org/downloads/)

---

## 安装 ManimGeo

### pip

```bash
# 仅安装数值计算
# 大部分情况下，几何构建都可以通过安装核心依赖完成
# 即使是使用 manimgl 或 janim 等动画库，也可以通过 Updater 等机制手动进行几何对象的关联更新
pip install manimgeo

# 安装 manimgl 集成
# 提供了一些 manimgl 工具
pip install manimgeo[manim]

# 安装 janim 集成
# 提供了一些 janim 工具
# 要求 janim[gui] >= 3.4.0
pip install manimgeo[janim]

# 提供了开发与测试工具，例如 pytest 与文档构建依赖
pip install manimgeo[dev]

# 全部安装
pip install manimgeo[full]
```

### uv（推荐）

若未安装 `uv`，通过以下命令安装

```bash
# 安装 uv
pip install uv
uv --version

# 创建虚拟环境
mkdir your/project/dir
cd your/project/dir
uv init
```

确认安装 `uv` 后，可通过 `uv` 安装 `manimgeo`

```bash
# 仅核心
uv add manimgeo
# 安装其它部件
uv add manimgeo --extra full
```

---

## 安装动画集成

根据你的需求，可以配置不同的动画引擎，因此以下的配置步骤都是**可选**的

### 安装 ManimGL

在官方文档阅读安装配置教程 👉 [ManimGL 安装配置指南](https://manimgl-zh.readthedocs.io/zh-cn/latest/getting_started/installation.html)

### 安装 JAnim

在官方文档阅读安装配置教程 👉 [JAnim 安装配置指南](https://janim.readthedocs.io/zh-cn/latest/tutorial/installation.html)
