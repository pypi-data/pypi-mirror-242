from setuptools import (
  find_packages,
  setup,
)

with open("README.md", "r") as file:
  long_description = file.read()

setup(
  name='pixiuquant',
  version='0.0.2',
  packages=find_packages(),
  author='pixiuquant',
  url='https://pypi.org/project/pixiuquant',
  description="pixiuquant 量化核心包",
  long_description=long_description,
  long_description_content_type="text/markdown",
  python_requires='>=3.10',
)
