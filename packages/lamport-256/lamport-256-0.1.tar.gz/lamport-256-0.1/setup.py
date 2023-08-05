import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()


setuptools.setup(
    name='lamport-256',
    version='0.1',
    author='JP Kiser',
    author_email='johnpaulkiser@gmail.com',
    description='Simple single use Lamport signature scheme',
    py_modules=["lamport_256"],
    package_dir={'': 'src'},
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/johnpaulkiser/lamport-256',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>3.6',
)
