import setuptools

# with open("README.md", "r", encoding = "utf-8") as fh:
#     long_description = fh.read()

setuptools.setup(
    name = "dynamixel_control",
    version = "0.1.0",
    author = "Kyle DuFrene",
    author_email = "dufrenekm@gmail.com",
    description = "Library for communicating with various Dynamixel motors.",
    # long_description = long_description,
    # long_description_content_type = "text/markdown",
    url = "https://github.com/OSUrobotics/dynamixel-control",
    # project_urls = {
    #     "Bug Tracker": "package issues URL",
    # },
    install_requires=["dynamixel_sdk>=3", "numpy"],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.6"
)
