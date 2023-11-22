from setuptools import setup,find_packages
setup(
    name='drawranflow',
    version='1.0.5',
    packages=find_packages(),
    package_data ={'drawranflow.servicelogic.intfconfig': ['*.json']},

    install_requires=[
        'Django~=4.2.7',
        'celery~=5.3.4',
        'pandas~=1.3.3',
        'pyshark~=0.6',

    ],
)
