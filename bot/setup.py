from setuptools import find_packages, setup

setup(
    name="bot",
    packages=find_packages(exclude=["bot_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "pandas",
        "numpy",
        "sklearn",
        "re",
        "pickle",
        "datetime",
        "python-dotenv",
        "os"
    ],
    extras_require={"dev": ["dagit", "pytest"]},
)
