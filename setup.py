from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="asistent-plant",
    version="0.1.0",
    author="Alex Han",
    description="AI-powered desktop automation agent with natural language understanding",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexjhan/asistent-plant",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.24.0",
        "pillow>=10.0.0",
        "opencv-python>=4.8.0",
        "pyautogui>=0.9.54",
        "pytesseract>=0.3.10",
        "transformers>=4.30.0",
        "torch>=2.0.0",
        "sentence-transformers>=2.2.0",
        "SpeechRecognition>=3.10.0",
        "mss>=9.0.0",
        "pygetwindow>=0.0.9",
        "pynput>=1.7.6",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0",
    ],
    entry_points={
        "console_scripts": [
            "asistent-plant=asistent_plant.main:main",
        ],
    },
)
