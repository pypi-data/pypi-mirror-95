﻿from setuptools import setup, find_packages
import io

import nheri_simcenter


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.md')

setup(
    name='nheri_simcenter',
    version=nheri_simcenter.__version__,
    url='http://nheri-simcenter.github.io/nheri_simcenter/',
    license='BSD License',
    author='Adam Zsarnóczay',
    tests_require=['pytest'],
    author_email='adamzs@stanford.edu',
    description='NHERI SimCenter Python Dependencies',
    long_description=long_description,
    long_description_content_type='text/markdown',
    #packages=['nheri_simcenter'],
    packages = find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=[
        'numpy>=1.19.0',
        'scipy>=1.5.0',
        'pandas>=1.1.0,<=1.1.5',
        'tables',
        'xlrd<=1.2.0',
        'openseespy',
        'sklearn',
        'jpype1',
        'tqdm'
    ],
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 5 - Production/Stable',
        'Natural Language :: English',
        'Environment :: Console',
        'Framework :: Jupyter',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering',
        ],
    extras_require={
        'testing': ['pytest'],
    }
)