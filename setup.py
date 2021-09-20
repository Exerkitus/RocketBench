import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rocketBench",
    version="0.0.1",
    author="Theo M",
    description="A toolbox-like package to aid with the design of liquid fuelled rocket engines, or really any constant mass-flow process.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="to be added later",
    project_urls={
        "Bug Tracker": "to be added later",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
)