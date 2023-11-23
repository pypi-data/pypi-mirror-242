from setuptools import find_packages, setup

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setup(
    name="kedro-expectations",
    version="0.2.3",
    url="https://gitlab.com/anacision-internal/kedro-great.git",
    author="Marcel Beining, based on work from Joao Gabriel Pampanin de Abreu",
    author_email="marcel.beining@anacision.de",
    description="Combine Kedro and Great Expectations",
    long_description="Combine Kedro and Great Expectations",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    license="MIT",
    install_requires=[
        "kedro~=0.18",
        "great_expectations>=0.17.12",
        "pandas",
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    entry_points={
        "kedro.global_commands": ["kedro-expectations = kedro_expectations:commands"]
    }
)
