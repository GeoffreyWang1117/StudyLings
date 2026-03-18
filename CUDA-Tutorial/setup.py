from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="jaxlings",
    version="0.1.0",
    author="JAXlings Contributors",
    description="Interactive JAX learning exercises with automatic grading",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/jaxlings",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "jax>=0.4.20",
        "jaxlib>=0.4.20",
        "numpy>=1.24.0",
        "pytest>=7.4.0",
        "colorama>=0.4.6",
        "watchdog>=3.0.0",
    ],
    entry_points={
        "console_scripts": [
            "jaxlings=jaxlings.cli:main",
        ],
    },
)
