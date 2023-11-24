import setuptools

# with open("README.md", "r", encoding = "utf-8") as fh:
#     long_description = fh.read()

setuptools.setup(
    name = "dynamixel-control",
    version = "0.0.1",
    author = "Kyle DuFrene",
    author_email = "dufrenekm@gmail.com",
    description = "short package description",
    # long_description = long_description,
    # long_description_content_type = "text/markdown",
    url = "https://github.com/OSUrobotics/dynamixel-control",
    # project_urls = {
    #     "Bug Tracker": "package issues URL",
    # },
    packages=setuptools.find_packages("dynamixel-sdk", "numpy"),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    # packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.6"
)
