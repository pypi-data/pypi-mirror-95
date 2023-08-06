from io import open

from setuptools import setup

# python setup.py sdist --formats=zip
# python setup.py sdist bdist_wheel
# twine upload dist/halolib-0.13.8.tar.gz -r pypitest
# twine upload dist/halo_bian-0.13.8.tar.gz -r pypi

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='halo-bian',
    version='0.12.41',
    packages=['halo_bian', 'halo_bian.bian','halo_bian.bian.plugins','halo_bian.bian.app',
              'halo_bian.bian.domain','halo_bian.bian.view','docs'],
    url='https://github.com/halo-framework/halo-bian',
    license='MIT License',
    author='halo-framework',
    author_email='halo-framework@gmail.com',
    description='this is the Halo Bian library',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ]
)
