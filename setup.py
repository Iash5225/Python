from setuptools import setup, find_packages

setup(
    name='UWA_Aerospace_Python',  # Name of your project
    version='0.1.0',  # Version number
    # This will discover your packages automatically
    packages=find_packages('scripts'),
    install_requires=[
        # List your project's dependencies here.
        # Examples:
        'numpy',
        'pandas',
        'matplotlib',
        'sympy'
    ],
    python_requires='>=3.6',  # Minimum version requirement of the package
    # You can also include other metadata such as:
    # description='A brief description of your project',
    # author='Your Name',
    # url='URL to your project repository or website',
)
