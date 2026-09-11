# -*- coding: utf-8 -*-
"""兼容旧工具链的 setup.py，实际元信息见 pyproject.toml。"""
from setuptools import find_packages, setup

setup(
    name="longcache",
    version="1.0.0",
    packages=find_packages(include=["longcache*"]),
    package_data={"longcache": ["models/cards/*.json"]},
    python_requires=">=3.9",
)
