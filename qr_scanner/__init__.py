"""
QR Scanner - A modern desktop application for scanning QR codes
Created using customtkinter and opencv-python
"""

from main import QRScannerApp

# Version of the qr_scanner package
__version__ = '1.0.0'

# Module level doc-string
__doc__ = """
QR Scanner - Modern QR Code Scanning Desktop Application
=====================================================

Description
-----------
A feature-rich desktop application for scanning QR codes using both file upload
and camera capture methods. Built with customtkinter for a modern user interface.

Main Features
------------
* File drag-and-drop support
* Live camera QR code scanning
* Dark/Light theme toggle
* Scan history tracking
* Copy to clipboard functionality
* Progress indication during scanning
"""

# Export the main application class
__all__ = ['QRScannerApp']