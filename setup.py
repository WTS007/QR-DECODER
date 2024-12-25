from setuptools import setup

setup(
    name="QR Scanner",
    version="1.0.0",
    description="A modern QR code scanner application",
    author="Your Name",
    packages=["qr_scanner"],
    install_requires=[
        "customtkinter>=5.2.0",
        "Pillow>=10.0.0",
        "opencv-python>=4.8.0.74",
        "pyzbar>=0.1.9",
        "pyperclip>=1.8.2",
    ],
    python_requires=">=3.7",
)