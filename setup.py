import setuptools

VERSION = "0.0.1"
DESCRIPTION = "Advent of Code helper package"

with open("README.md", "r") as F:
    LONG_DESCRIPTION = F.read()

setuptools.setup(
    name="adventofcode",
    version=VERSION,
    author="Manuel Cordova",
    author_email="manucordova@bluewin.ch",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
)
