from pathlib import Path
import sys
import subprocess

source_dir = Path(__file__).parent
src_dir = source_dir.parent.parent / 'src'
sys.path.insert(0, str(src_dir))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'ManimGeo'
copyright = '2025, LifeCheckpoint'
author = 'LifeCheckpoint'
release = '1.3.0a2'

html_theme = "furo"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

templates_path = ['_templates']
exclude_patterns = []

language = 'zh-cn'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_static_path = ['_static']

extensions = [
    'myst_parser',
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autodoc',          # 自动从代码中提取文档
    'sphinx.ext.napoleon',         # 支持 NumPy 和 Google 风格的 docstrings
    'sphinx.ext.autosummary',      # 自动生成模块、类、函数摘要
    'sphinx.ext.viewcode',         # 在文档中添加源代码链接
    'sphinx.ext.todo',             # 支持 TODO 列表
    'sphinx.ext.mathjax',          # 支持数学公式
    'sphinx.ext.ifconfig',         # 条件包含内容
    'sphinx_autodoc_typehints',    # 增强类型注解的显示
]

# autodoc 配置
autodoc_member_order = 'bysource'  # 成员按源代码中的顺序排列
autodoc_default_options = {
    'members': True,               # 默认显示所有成员
    'undoc-members': False,         # 默认显示没有 docstring 的成员
    'show-inheritance': True,      # 默认显示继承关系
}

# autosummary 配置
autosummary_generate = True
autosummary_imported_members = True

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# Generate API documentation
# sphinx-apidoc -o source/apidoc ../src/manimgeo --separate --force -d 6 

try:
    subprocess.run(
        [
            'sphinx-apidoc',
            '-o', str(source_dir / "apidoc"),
            str(src_dir / 'manimgeo'),
            '--separate',
            '--force',
            '-d', '6'
        ],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
except subprocess.CalledProcessError as e:
    print(f"生成 API 文档错误: {e}")