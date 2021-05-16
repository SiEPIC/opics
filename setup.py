from setuptools import setup, find_packages


def get_install_requires():
    with open("requirements.txt", "r") as f:
        return [line.strip() for line in f.readlines() if not line.startswith("-")]


with open("README.rst") as readme_file:
    readme = readme_file.read()


setup(
    author="Jaspreet Jhoja",
    author_email="jaspreet@siepic.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Open-source frequency domain solver for photonic integrated circuits.",
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords="opics",
    name="opics",
    packages=find_packages(),
    install_requires=get_install_requires(),
    test_suite="tests",
    url="https://github.com/siepic/opics",
    version="0.1.7",
    zip_safe=False,
)
