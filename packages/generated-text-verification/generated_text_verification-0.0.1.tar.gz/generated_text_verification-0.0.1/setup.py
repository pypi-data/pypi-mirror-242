from setuptools import find_packages, setup

install_requires = [
    "nltk==3.8.1",
    "numpy",
    "pydash",
    "sentence-transformers==2.2.2",
]

setup(
    name="generated_text_verification",
    version="0.0.1",
    author="Kuuhaku",
    author_email="kuuhaku.work@gmail.com",
    description="A package comprising functions designed for the validation of rewritten texts",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ManhDzungNguyen/generated_text_verification",
    package_dir={"": "src"},
    packages=find_packages("src"),
    zip_safe=False,
    python_requires=">=3.8.0",
    install_requires=install_requires,
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
