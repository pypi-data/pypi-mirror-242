from setuptools import setup

with open("README.md") as f:
    markdown_description = f.read()

with open("scripts/requires.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="pyxreader",
    version="0.0.1",
    author="ashgw",
    author_email="AshrefGw@proton.me",
    url="https://github.com/AshGw/pyxreader.git",
    description="A versatile module providing memory-efficient text-to-speech capabilities for various file formats.",
    long_description_content_type="text/markdown",
    long_description=markdown_description,
    python_requires=">=3.10",
    package_data={
        "pyxreader": ["**"],
    },
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.10",
    ],
)
