from setuptools import setup, find_packages

setup(
    name='cvrmap',
    version='2.0.6',
    url='https://github.com/ln2t/cvrmap',
    author='Antonin Rovai',
    author_email='antonin.rovai@hubruxelles.be',
    description='CVRmap is an opensource software to compute maps of Cerebro-Vascular Reactivity',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'cvrmap = cvrmap.cvrmap:main',
        ]}
)
