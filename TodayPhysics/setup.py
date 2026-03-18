#!/usr/bin/env python3
"""
Physics Rustlings - Setup Script
"""

from setuptools import setup, find_packages

setup(
    name="physics-rustlings",
    version="1.0.0",
    description="An interactive physics learning tool through programming",
    author="Physics Rustlings Team",
    python_requires=">=3.9",
    packages=find_packages(),
    install_requires=[
        "studylings>=0.1.0",
        "numpy>=1.24.0",
        "scipy>=1.10.0",
        "sympy>=1.12",
        "matplotlib>=3.7.0",
        "rich>=13.0.0",
        "click>=8.1.0",
        "watchdog>=3.0.0",
    ],
    extras_require={
        "full": [
            "plotly>=5.14.0",
            "qutip>=4.7.0",
            "einsteinpy>=0.4.0",
            "py-pde>=0.30.0",
            "manim>=0.17.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "physics-rustlings=todayphysics.__main__:_main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Physics",
    ],
)
