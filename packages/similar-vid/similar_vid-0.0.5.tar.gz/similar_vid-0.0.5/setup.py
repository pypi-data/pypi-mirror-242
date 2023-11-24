import os

from setuptools import setup, find_packages

setup(
    name='similar_vid',
    version='0.0.5',
    url='https://github.com/supermakc/similar-vid',
    license='MIT',
    author='Maxim Baryshev',
    author_email='supermakc@gmail.com',
    description='Similar-vid is a library for finding similar frames between videos',
    packages=find_packages(),
    keywords='video similar skip intro',
    install_requires=['decord',
                      'ImageHash',
                      'numpy',
                      'opencv-python',
                      'Pillow',
                      'PyWavelets',
                      'scipy',
                      ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10'
    ]
)
