from setuptools import setup, find_packages

setup(
   name='exemple-package',
    version="0.0.1",
    author="Baouly Nelson",
    author_email="baoulynelson@egmail.com",
    description="Un petit exemple de package",
    install_requires=[
    ],
    url="https://github.com/BaoulyNelson/packagingutorial.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
)
