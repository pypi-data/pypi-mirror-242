from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name="PrintString",
    version='0.0.1',
    description="It will print a string",
    long_description=open("README.txt").read() + '\n\n' + open("CHANGELOG.txt").read(),
    url="",
    author="Arjun Patel",
    author_email="arjunbrij8811@gmail.com",
    license="MIT",
    classifiers=classifiers,
    keywords="Print",
    packages=find_packages(),
    install_requires=[""]
)