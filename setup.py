from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="advanced-pest-detection",
    version="0.1.0",
    author="Ali Rizvi",
    author_email="alirizvi277.ar@gmail.com",
    description="Advanced Agricultural Pest Detection and Prediction System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ali-Rizvi-1/advanced_pest_detection",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy",
        "opencv-python",
        "ultralytics",
        "omegaconf",
        # Add other dependencies here
    ],
)