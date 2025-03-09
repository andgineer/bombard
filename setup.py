import setuptools

with open("README.rst", encoding="utf8") as fh:
    long_description = fh.read()

with open("requirements.in", encoding="utf8") as f:
    requirements = f.read().splitlines()

import sys

sys.path.insert(0, "../")
import bombard

setuptools.setup(
    name="bombard",
    version=bombard.version(),
    # scripts=['bin/bombard'],
    entry_points={
        "console_scripts": [
            "bombard=bombard.main:main",
        ],
    },
    author="Andrey Sorokin",
    author_email="filbert@yandex.ru",
    description="Stress testing servers with easily configurable requests.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://bombard.sorokin.engineer",
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires=">=3.10",
    install_requires=requirements,
    keywords="http load test parallel",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
