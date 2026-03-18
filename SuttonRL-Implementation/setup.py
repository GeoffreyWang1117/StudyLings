from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sutton-rl",
    version="0.1.0",
    author="Your Name",
    description="Interactive exercises for Sutton & Barto's RL book",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GeoffreyWang1117/SuttonRL-Implementation",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "matplotlib>=3.4.0",
        "scipy>=1.7.0",
        "gym>=0.21.0",
        "tqdm>=4.62.0",
        "colorama>=0.4.4",
        "pyyaml>=6.0",
    ],
    entry_points={
        "console_scripts": [
            "sutton-rl=sutton_rl.runner:main",
        ],
    },
)
