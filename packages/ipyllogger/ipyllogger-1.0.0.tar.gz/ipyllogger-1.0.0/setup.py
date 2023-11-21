import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
	name="ipyllogger",
	version="1.0.0",
    author="Makendy ALEXIS",
	author_email="makendyalexis5414@gmail.com",
	description="[SCHOOL PROJECT - PYTHON BASICS] | Minimum Python package to write logs in a file",
    maintainer="Louis Midson LAJEANTY",
    maintainer_email="mds@louismidson.me",
	long_description=long_description,
	long_description_content_type='text/markdown',
	url="https://github.com/RagnarBob/Ilogger",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	install_requires=[],
	python_requires='>=3.8, <4',
)