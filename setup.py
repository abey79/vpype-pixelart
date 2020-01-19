from setuptools import setup, find_packages


with open("README.md") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()

setup(
    name="vpype-pixelart",
    version="0.1.0",
    description="",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Antoine Beyeler",
    url="",
    license=license,
    packages=find_packages(exclude=("examples", "tests")),
    install_requires=[
        'click',
        'imageio',
        'vpype @ git+https://github.com/abey79/vpype.git',
    ],
    entry_points='''
            [vpype.plugins]
            pixelart=pixelart.pixelart:pixelart
        ''',
)
