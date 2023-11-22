from setuptools import setup

dependencies = [
    'pandas',
    'numpy'
  ]

VERSION = "0.0.1"

setup(
    name='inferencia_causal',
    packages=['inferencia_causal'],
    version=VERSION,
    license='MIT License',
    description='Tecnicas de inferencia',
    long_description='Tecnicas de inferencia',
    author='Kleber Jorge Santos',
    # url='https://github.com/KleberJorgeSantos/inference',
    # download_url='https://github.com/KleberJorgeSantos/inference/archive/{}.tar.gz'.format(VERSION),
    keywords=['logistic', 'regression', 'matching', 'observational', 'study', 'causal', 'inference'],
    include_package_data=True,
    install_requires=dependencies
    )
