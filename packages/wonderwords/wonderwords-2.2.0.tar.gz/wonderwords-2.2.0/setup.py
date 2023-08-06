import setuptools

with open("PYPI.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wonderwords",
    version="2.2.0",
    author="Maxim Rebguns",
    author_email="mrmaxguns@gmail.com",
    include_package_data=True,
    description=(
        "A python package for random words and sentences in the english"
        " language"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mrmaxguns/wonderwordsmodule",
    packages=setuptools.find_packages(),
    install_requires=[
        'importlib_resources == 5.1.0; python_version < "3.7"',
    ],
    extras_require={"cli": ["rich == 9.10.0"]},
    package_data={"wonderwords": ["assets/*.txt"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": ["wonderwords = wonderwords.cmdline_parser:main"]
    },
)
