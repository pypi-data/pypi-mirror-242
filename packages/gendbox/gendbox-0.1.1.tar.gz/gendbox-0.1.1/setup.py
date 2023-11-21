from setuptools import setup, find_packages

setup(
    name='gendbox',
    version='0.1.1',
    description='Açıklama',
    author='Candaş Koru',
    packages=find_packages(exclude=['gendbox.learning']),
    install_requires=[
        'numpy',
        'pandas'
    ],
)