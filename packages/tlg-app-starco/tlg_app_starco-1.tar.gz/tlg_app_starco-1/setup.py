from setuptools import setup,find_packages
requires = [
    'Starco==2.3.2',
    'Telethon==1.32.1'
]

setup(
    name = 'tlg_app_starco',
    version='1',
    author='Mojtaba Tahmasbi',
    packages=find_packages(),
    install_requires=requires,
)