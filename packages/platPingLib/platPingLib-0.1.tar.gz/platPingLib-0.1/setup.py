from setuptools import setup, find_packages

setup(
    name='platPingLib',
    version='0.1',
    packages=find_packages(),
    description='A simple ping library for Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Caleb Finigan',
    author_email='cfinigan@outlook.com',
    url='https://github.com/CalebFin/PlatPingLib',
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)