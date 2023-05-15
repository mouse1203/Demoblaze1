from setuptools import setup

setup(
    name='Demoblaze',
    version='1.0.0',
    install_requires=[
        'pytest >= 7.3.1',
        'pytest-asyncio >= 0.21.0',
        'pytest-playwright >=  0.3.3',
        'pytest-reporter >=  0.5.2',
        'pytest-reporter-html1 >= 0.8.2',
        'playwright >= 1.33.0',
        'pytest-progress >=1.2.5',
    ],
)    