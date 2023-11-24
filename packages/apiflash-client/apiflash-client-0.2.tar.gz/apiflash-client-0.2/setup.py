
import os
import setuptools

def readme():
    path = os.path.dirname(__file__)
    with open(os.path.join(path, 'README.rst')) as f:
        return f.read()

name = 'apiflash-client'
description = 'ApiFlash.com Client'
version = '0.2'
author = 'Fictive Kin LLC'
email = 'hello@fictivekin.com'
classifiers = [
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Topic :: Software Development',
]

if __name__ == "__main__":
    setuptools.setup(
        name=name,
        version=version,
        description=description,
        long_description=readme(),
        classifiers=classifiers,
        url='https://github.com/fictivekin/apiflash-client',
        author=author,
        author_email=email,
        maintainer=author,
        maintainer_email=email,
        license='MIT',
        python_requires=">=3.7",
        packages=[
            'apiflash',
        ],
        install_requires=[
            'api-client',
            'click',
        ],
        scripts=[
            'bin/apiflash',
        ],
    )
