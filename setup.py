from setuptools import setup, find_packages

setup(
    name="yt-shorts-analyzer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "google-api-python-client==2.177.0",
        "google-generativeai==0.8.5",
        "python-dotenv==1.1.1",
        "streamlit==1.37.0",
    ],
    entry_points={
        "console_scripts": [
            "yt-shorts-analyzer=app:main",
        ],
    },
)