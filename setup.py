import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="triton-slode",
    version="0.0.1",
    author="Stian Lode",
    author_email="stian.lode@gmail.com",
    description="A framework for toying with 2D game physics.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/slode/triton",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
