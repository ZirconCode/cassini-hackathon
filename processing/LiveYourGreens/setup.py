from setuptools import setup

setup(
    name='LiveYourGreens',
    version='0.0.0',
    description='',
    long_description_content_type='text/x-rst',
    author='Live Your Greens Team',
    packages=['lyg'],
    include_package_data=True,
    install_requires=['numpy',
                      'pyhdf',
                      'matplotlib',
                      'rasterio',
                      'scikit-image',
                      'tqdm',
                      'scipy',
                      'pandas',
                      'seaborn'],
    license='',
    zip_safe=False,
    keywords='liveyourgreens',
    python_requires='~=3.8',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
    ]
)
