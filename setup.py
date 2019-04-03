import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='bombard',
    version='1.0',
    scripts=['bin/bombard'],
    # entry_points={
    #     'console_scripts': [
    #         'bombard=bombard.main:main',
    #     ],
    # },
    author="Andrey Sorokin",
    author_email="filbert@yandex.ru",
    description="Bombards target server with simultaneous requests",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/masterandrey/bombard",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'pyyaml>=5.1',
    ],
    keywords='http load test parallel',
    classifiers=[
     "Programming Language :: Python :: 3",
     "License :: OSI Approved :: MIT License",
     "Operating System :: OS Independent",
    ],
 )