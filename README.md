# PDF Hub - Desktop Application

A cross-platform desktop application for PDF operations built with Python and pywebview.

## Features

- **Merge PDFs**: Combine multiple PDF files into one
- **Split PDF**: Extract specific pages from a PDF
- **Compress PDF**: Reduce PDF file size
- **Image to PDF**: Convert images (JPG, PNG, etc.) to PDF
- **PDF to Text**: Extract text content from PDFs

## Installation

1. Create a virtual environment:
```bash
python3 -m venv venv
```

2. Activate the virtual environment:
```bash
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python main.py
```

Or use the provided run script:
```bash
./run.sh  # On macOS/Linux
# or
run.bat  # On Windows
```

## Project Structure

```
pdf-hub/
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── backend/
│   ├── __init__.py
│   └── pdf_service.py   # PDF operations service
└── ui/
    ├── index.html       # Dashboard
    ├── merge.html       # Merge PDFs screen
    ├── split.html       # Split PDF screen
    ├── compress.html    # Compress PDF screen
    ├── img_to_pdf.html  # Image to PDF screen
    └── pdf_to_text.html # PDF to Text screen
```

## Technology Stack

- **Python 3**
- **pywebview** - Native desktop window
- **PyPDF2** - PDF operations
- **Pillow** - Image processing
- **Tailwind CSS** - UI styling

## License

MIT
