"""
Setup script for the studylings shared framework.
"""

from setuptools import setup, find_packages

setup(
    name="studylings",
    version="0.1.0",
    author="Studylings Team",
    description="Shared framework for rustlings-style educational projects",
    python_requires=">=3.9",
    packages=find_packages(include=["studylings", "studylings.*"]),
    install_requires=[
        "click>=8.1.0",
        "rich>=13.0.0",
        "watchdog>=3.0.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
