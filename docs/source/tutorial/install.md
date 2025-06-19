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
pip install manimgeo

# 安装 manimgl 集成
pip install manimgeo[manim]

# 安装 janim 集成
pip install manimgeo[janim]

# 全部安装
pip install manimgeo[full]
```

### uv（推荐）

若未安装 `uv`，通过以下命令安装

```bash
pip install uv
```

确认安装 `uv` 后，可通过 `uv` 安装 `manimgeo`

```bash
uv add manimgeo[full]
```

~~目前未发布到 Pypi~~

### 离线安装

假设你已经下载了 `manimgeo.xx.whl`，执行：

```bash
pip install manimgeo.xx.whl
```

---

## 安装动画集成

根据你的需求，可以安装不同的动画引擎，因此以下的安装步骤都是**可选**的

### 安装 ManimGL

访问官方文档阅读安装教程 👉 [ManimGL 安装指南](https://manimgl-zh.readthedocs.io/zh-cn/latest/getting_started/installation.html)

### 安装 JAnim

访问官方文档阅读安装教程 👉 [JAnim 安装指南](https://janim.readthedocs.io/zh-cn/latest/tutorial/installation.html)
