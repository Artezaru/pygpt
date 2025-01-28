import os
from setuptools import setup, find_packages

# Read the contents of your README file to use as the long description
with open("README.md", "r") as fh:
    long_description = fh.read()

# Read the contents of your requirements.txt
def read_requirements():
    with open('requirements.txt') as f:
        # Remove comments and empty lines
        return [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]

# Read the version in the __version__.py file
def read_version():
    version_file = os.path.join(os.path.dirname(__file__), 'pygpt', '__version__.py')
    with open(version_file) as f:
        exec(f.read()) 
    return locals()['__version__']

setup(
    name="pygpt",  # Replace with your package name
    version=read_version(),  # Update the version as necessary
    author="Artezaru",  # Your name
    author_email="artezaru.github@proton.me",  # Your email
    description="Chat GPT with command line",  # Short description of the package
    long_description=long_description,  # Read the long description from README
    long_description_content_type="text/markdown",  # Format of the long description
    url="https://github.com/Artezaru/pygpt.git",  # URL to the project repository
    packages=find_packages(),  # Automatically find packages in the directory
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Minimum Python version required
    install_requires=read_requirements(),
    entry_points={
        'console_scripts': [
            'pygpt = pygpt.__main__:main',  # Define the pygpt command to run main()
        ],
    },
)

