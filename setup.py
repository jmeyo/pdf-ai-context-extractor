from setuptools import setup, find_packages

setup(
    name="pdf-ai-context-extractor",
    version="0.5.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "tabula-py>=2.0.0",
        "pandas>=1.3.0",
    ],
    entry_points={
        "console_scripts": [
            "pdf-extract=pdf_ai_context_extractor.cli:main",
        ],
    },
)
