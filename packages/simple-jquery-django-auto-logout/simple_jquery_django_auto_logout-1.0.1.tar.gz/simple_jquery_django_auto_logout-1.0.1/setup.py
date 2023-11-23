from setuptools import find_packages, setup

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setup(
    name = "simple_jquery_django_auto_logout",
    version = "1.0.1",
    author = "Aditya Yudhi Hanafi",
    author_email = "adityayudhi10@gmail.com",
    description = "Simple Jquery-Django autologout system",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://gitlab.com/adityayudhi/simple_jquery_django_auto_logout",
    project_urls = {
        "Bug Tracker": "https://gitlab.com/adityayudhi/simple_jquery_django_auto_logout/-/issues",
        "repository" : "https://gitlab.com/adityayudhi/simple_jquery_django_auto_logout",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages = find_packages(),
    python_requires = ">=3.6"
)
