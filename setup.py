from setuptools import setup

with open("README.md") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()

setup(
    name="vpype-pixelart",
    version="0.1.0",
    description="Pixel art plug-in for vpype",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Antoine Beyeler",
    url="https://github.com/abey79/vpype-pixelart",
    packages=["pixelart"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Topic :: Multimedia :: Graphics",
        "Environment :: Plugins",
    ],
    setup_requires=["wheel"],
    install_requires=[
        "click",
        "imageio",
        "numpy",
        "vpype[all]>=1.10,<2.0",
    ],
    entry_points="""
            [vpype.plugins]
            pixelart=pixelart.pixelart:pixelart
        """,
)
