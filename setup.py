from setuptools import setup


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
    packages=["pixelart"],
    install_requires=[
        'click',
        'imageio',
        'numpy',
        'vpype[all]>=1.7',
    ],
    entry_points='''
            [vpype.plugins]
            pixelart=pixelart.pixelart:pixelart
        ''',
)
