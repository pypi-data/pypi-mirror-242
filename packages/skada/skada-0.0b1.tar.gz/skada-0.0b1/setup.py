from setuptools import setup, find_packages

setup(
    name='skada',
    version='0.0b1',
    description='Domain adaptation toolbox compatible with scikit-learn.',

    # The project's main homepage.
    url='https://github.com/scikit-adaptation/skada',

    # Author details
    author='Théo Gnassounou, Rémi Flamary',
    author_email='theo.gnassounou@inria.fr, remi.flamary@polytechnique.edu',

    # Choose your license
    license='BSD 3-Clause',
    # What does your project relate to?
    keywords='da deep-learning',

    packages=find_packages(),
)
