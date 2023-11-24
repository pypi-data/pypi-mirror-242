from setuptools import setup, find_packages

setup(
    name='alpacaz',
    version='0.2',
    packages=find_packages(),
    author='Lalith Kumar Shiyam Sundar, Zacharias Chalampalakis',
    author_email='Lalith.shiyamsundar@meduniwien.ac.at',
    url='',  # Add your package's homepage URL here
    description='',  # Add a short description of the package here
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[],  # List your package's dependencies here
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.10',
)
