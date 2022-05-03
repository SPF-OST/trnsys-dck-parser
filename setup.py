import setuptools  # type: ignore[import]


setuptools.setup(
    name="trnsys_dck_parser",
    author="Institute for Solar Technology (SPF), OST Rapperswil",
    author_email="damian.birchler@ost.ch",
    description="A parser for TRNSYS deck files",
    url="https://github.com/SPF-OST/trnsys_dck_parser",
    packages=setuptools.find_packages(),
    package_dir={"":"src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
