# QR Scanner

A modern, feature-rich desktop application for scanning QR codes. Built with Python and customtkinter, this application provides an intuitive interface for scanning QR codes through both file upload and camera capture methods.

## Features

- **Modern User Interface**: Clean, intuitive design with customtkinter
- **Multiple Scanning Methods**:
  - File upload with drag-and-drop support
  - Live camera capture
- **Advanced Features**:
  - Dark/Light theme toggle
  - Scan history tracking
  - Copy results to clipboard
  - Progress indication during scanning
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Installation

### Using pip

```bash
pip install qr-scanner
```

### From source

1. Clone the repository:
```bash
git clone https://github.com/yourusername/qr-scanner.git
cd qr-scanner
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Install the package:
```bash
pip install .
```

## Usage

### Running the Application

After installation, you can run the application in two ways:

1. From the command line:
```bash
qr-scanner
```

2. From Python:
```python
from qr_scanner import QRScannerApp

app = QRScannerApp()
app.run()
```

### Using the Application

1. **File Upload Method**:
   - Click the "Choose File" button or drag and drop an image file containing a QR code
   - The application will automatically process the image and display the decoded content

2. **Camera Capture Method**:
   - Switch to the "Camera" tab
   - Click "Start Camera" to begin the camera feed
   - Position the QR code in front of the camera
   - Click "Capture" to scan the QR code

3. **Additional Features**:
   - Use the theme toggle button in the top-right corner to switch between light and dark modes
   - Click "Copy to Clipboard" to copy the decoded content
   - View your scan history in the bottom section of the application

## Requirements

- Python 3.7 or higher
- Operating System: Windows 7 or higher, macOS 10.13 or higher, or Linux with GTK 3
- Camera (optional, for live scanning)

## Development

### Setting Up Development Environment

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

### Running Tests

```bash
python -m pytest tests/
```

### Building Executable

Using PyInstaller:

```bash
pyinstaller qr_scanner.spec
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [customtkinter](https://github.com/TomSchimansky/CustomTkinter) for the modern UI components
- [opencv-python](https://github.com/opencv/opencv-python) for camera capture functionality
- [pyzbar](https://github.com/NaturalHistoryMuseum/pyzbar) for QR code decoding
- All contributors who have helped with bug fixes and improvements

## Support

If you encounter any issues or have questions:

1. Check the [FAQ](docs/FAQ.md)
2. Search existing [issues](https://github.com/yourusername/qr-scanner/issues)
3. Create a new issue if needed

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes in each release.