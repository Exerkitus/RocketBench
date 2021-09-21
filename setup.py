from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="rocketBench",
    version="0.0.2",
    author="Theo M",
    description="A toolbox-like package to aid with the design of liquid fuelled rocket engines, or really any constant mass-flow process.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Exerkitus/RocketBench",
    project_urls={
        "Bug Tracker": "https://github.com/Exerkitus/RocketBench/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages= find_packages(), #[ "src", "src.FluidSubclasses", "src.PortSubclasses" ]
    python_requires=">=3.9",
)