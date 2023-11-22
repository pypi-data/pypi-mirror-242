"""Install SciencePlots.

This script (setup.py) will install the SciencePlots package.
In order to expose .mplstyle files to matplotlib, "import scienceplots"
must be called before plt.style.use(...).
"""

import os
from setuptools import setup

# Get description from README
root = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(root, 'README.md'), 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ideplots',
    version='0.1.0',
    author="Ben Abernathy",
    author_email="ben.abernathy@gmail.com",
    maintainer="Ben Abernathy",
    maintainer_email="ben.abernathy@gmail.com",
    description="Format Matplotlib for easy viewing in IDEs",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="MIT",
    url="https://github.com/benabernathy/ideplots/",

    install_requires=['matplotlib'],
    packages=["ideplots"],
    package_data={
      'ideplots': ['styles/**/*.mplstyle'],
    },

    classifiers=[
        'Framework :: Matplotlib', 
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    keywords=[
        "matplotlib-style-sheets",
        "matplotlib-figures",
        "matplotlib-styles",
        "python"
    ],
)