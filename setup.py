import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="manimgeo",
    version="1.0.1",
    author="lifechpt",
    url='',
    author_email="lifechpt@qq.com",
    description="A library for Geometry constructing and animation generating",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.10",
)
