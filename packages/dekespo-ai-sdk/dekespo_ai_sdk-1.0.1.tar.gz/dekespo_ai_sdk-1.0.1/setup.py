from setuptools import setup, find_packages

setup(
    name="dekespo_ai_sdk",
    packages=find_packages(include=("dekespo_ai_sdk*",)),
    version="1.0.1",
    license="apache-2.0",
    description="Dekesp AI SDK tools",
    author="Deniz Kennedy",
    author_email="deniz.kennedy@gmail.com",
    url="https://github.com/dekespo/dekespo_ai_sdk_py",
    keywords=["SDK", "AI", "Tool"],
    install_requires=[],
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)