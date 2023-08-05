import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='pypypy',  
     version='0.1',
     author="Ayumu098",
     author_email="stephen.singer.098@gmail.com",
     description="A test package for learning how to upload better in pip",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/Ayumu098/pypypy",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )