from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'A Machine Learning Library for the noobies'
LONG_DESCRIPTION = 'A package that allows to get the classification and test results of machine learning algorithm'

# Setting up
setup(
    name="amey_ml",
    version=VERSION,
    author="Amey Shinde",
    author_email="<amey.shinde@bizzencecollab.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy', 'tensorflow', 'pandas','scikit-learn','keras'],
    keywords=['python', 'machinelearning'],
    classifiers=[]
)