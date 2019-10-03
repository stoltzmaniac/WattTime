import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="watttime",
    version="0.0.3",
    author="Scott Stoltzman",
    author_email="scott@stoltzmanconsulting.com",
    description="A package to access the WattTime API v2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stoltzmaniac/WattTime",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests'
    ],
)