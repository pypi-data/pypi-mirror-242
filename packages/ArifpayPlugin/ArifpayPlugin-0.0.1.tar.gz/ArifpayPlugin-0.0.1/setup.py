from setuptools import find_packages, setup

with open("./README.md", "r") as f:
    long_description = f.read()

setup(
    name="ArifpayPlugin",
    version="0.0.1",
    description="Python Plug in for Arifpay",
    package_dir={"": "plugin"},
    packages=find_packages(where="plugin"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AnaniyaBelew",
    author="Ananiya Belew",
    author_email="anewscho@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=["uuid","requests","python-dotenv"],
    python_requires=">=3.10",
)