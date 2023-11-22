from setuptools import setup, find_packages

setup(
    name='matlib_Pirate_Wolf',
    version='0.1',
    packages=find_packages(include=['matlib_Pirate_Wolf', 'matlib_Pirate_Wolf.*']),
    description='A small math library',
    author='Pedro Santos',
    author_email='pedroshiva.santos2@gmail.com',
    url='http://github.com/PedroSantos/matlib_Pirate_Wolf',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)