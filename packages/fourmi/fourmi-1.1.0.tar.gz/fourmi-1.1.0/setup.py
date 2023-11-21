from setuptools import setup, find_packages


VERSION = '1.1.0'
DESCRIPTION = 'A parcelled package for text formats.'
LONG_DESCRIPTION = 'A package that allows to format text to make fancy text outputs for developers in their programs.'


setup(
    name="fourmi",
    version=VERSION,
    author="MrDark",
    author_email="<darkmr297@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'format', 'colors', 'colours', 'text format', 'rgbpyth'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
