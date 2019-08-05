from pathlib import Path

from setuptools import setup

current_dir = Path(__file__).parent.resolve()

with open(current_dir / "README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="inspectortiger",
    version="0.2.0",
    packages=["inspectortiger"],
    url="https://github.com/thg-consulting/inspectortiger",
    author="thg",
    requirements=["reportme"],
)