import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="barkus-func-toolkit", 	# This is the name of the package
    version="0.0.2",                        		# The initial release version
    author="barkustech",                     		# Full name of the author
    description="Cloud Functions Toolkit",
    long_description=long_description,      		# Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    		# List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: Free For Educational Use",
        "Operating System :: OS Independent",
    ],                                      		# Information to filter the project on PyPi website
    python_requires='>=3.10',                		# Minimum version requirement of the package
    py_modules=["barkus_function_toolkit"],             	# Name of the python package
    # package_dir={'':'barkus_function_toolkit'},   	# Directory of the source code of the package
    install_requires=[
        "cloudevents==1.9.0",
        "functions-framework==3.3.0",
        "pydantic==1.10.7",
        "python-dateutil==2.8.2",
        "requests==2.28.2",
        "dacite==1.8.1",
    ],
    extras_require = {
        "pubsub": [
            "google-api-core==2.11.0",
            "google-auth==2.17.0",
            "google-cloud-core==2.3.2",
            "google-cloud-pubsub==2.9.0"
        ],
        "bigquery": [
            "google-api-core==2.11.0",
            "google-auth==2.17.0",
            "google-cloud-core==2.3.2",
            "google-cloud-bigquery==3.10.0"
        ],
        "firestore": [
            "google-api-core==2.11.0",
            "google-auth==2.17.0",
            "google-cloud-core==2.3.2",
            "google-cloud-firestore==2.10.1"
        ],
        "test": [
            "polyfactory==2.2.0",
            "pytest==7.2.2",
            "pytest-cov==4.0.0",
            "pytest-mock==3.10.0",
            "pytest-watch==4.2.0",
            "mock_firestore==0.11.0",
        ]
    }
)