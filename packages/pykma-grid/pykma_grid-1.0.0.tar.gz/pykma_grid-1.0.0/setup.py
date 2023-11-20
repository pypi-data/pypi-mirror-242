from setuptools import setup, find_packages

setup(
    name="pykma_grid",
    version="1.0.0",
    author="Jeong Gaon",
    author_email="gokirito12@gmail.com",
    description="A Python package for converting latitude and longitude to grid coordinates using Lambert Conformal Conic Projection",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/gaon12/pykma_grid",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
