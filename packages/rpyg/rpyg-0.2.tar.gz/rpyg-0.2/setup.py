import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='rpyg',  
     version='0.2',
     author="Ayumu098",
     author_email="stephen.singer.098@gmail.com",
     description="A Python3 library implementation of a general role playing game system",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/Ayumu098/rpg",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )