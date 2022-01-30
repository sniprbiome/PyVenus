import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyVenus", # Replace with your own username
    version="0.0.1",
    author="Benjamin Wohl",
    author_email="benjaminwohl@gmail.com",
    description="Python interface to interact with Hamilton robots via Venus",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License",
        "Operating System :: Microsoft Windows",
    ],
    python_requires='>=3.6',
)