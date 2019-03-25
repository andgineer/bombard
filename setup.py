import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='bombard',
     version='0.1',
     scripts=['bombard'] ,
     author="Andrey Sorokin",
     author_email="filbert@yandex.ru",
     description="Bombard target server with simultaneous requests",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/masterandrey/bombard",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )