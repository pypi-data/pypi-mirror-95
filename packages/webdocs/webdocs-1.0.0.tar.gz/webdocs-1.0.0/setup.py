import setuptools

with open('README.rst') as f:
    long_description = f.read()

setuptools.setup(
    name='webdocs',
    version='1.0.0',
    author='Abraham',
    author_email='abraham.liu@hotmail.com',
    description='small tool to generate openapi doc',
    install_requires=['PyYAML'],
    long_description=long_description,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
