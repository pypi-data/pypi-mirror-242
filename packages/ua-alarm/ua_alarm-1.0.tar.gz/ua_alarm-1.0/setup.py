import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ua_alarm",
    author="user-sspmynxdvb",
    version="1.0",
    description="Implements api.ua_alarm.com API that returns info about Ukraine air raid alarms.",
    license="GNUv3",
    url="https://github.com/user-sspmynxdvb/ua_alarm",
    packages=setuptools.find_packages(),
    install_requires=[
        'aiohttp', 'pydantic'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)