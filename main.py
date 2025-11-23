"""
PDF Hub - Desktop Application
Main entry point for the pywebview desktop application.
"""

import os
import webview
import logging
from pathlib import Path
from backend import PdfService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the directory containing this script
BASE_DIR = Path(__file__).parent
UI_DIR = BASE_DIR / 'ui'


class Api:
    """
    JavaScript-Python API bridge.
    Exposes methods to the frontend via window.pywebview.api
    """

    def __init__(self):
        self.pdf_service = PdfService()
        self.window = None
        logger.info("API initialized")

    def set_window(self, window):
        """Set the webview window reference."""
        self.window = window

    def merge_pdfs(self, files, output_name=None):
        """
        Merge multiple PDF files into one.
        
        Args:
            files: List of file paths to merge
            output_name: Optional output filename (defaults to 'merged.pdf')
            
        Returns:
            dict: {"success": bool, "output": str, "error": str}
        """
        try:
            if not files or len(files) == 0:
                return {"success": False, "error": "No files selected"}
            
            # Default output name
            if not output_name:
                output_name = "merged.pdf"
            
            # Ask user where to save
            save_path = self.window.create_file_dialog(
                webview.SAVE_DIALOG,
                save_filename=output_name,
                file_types=('PDF Files (*.pdf)',)
            )
            
            if not save_path:
                return {"success": False, "error": "Save cancelled"}
            
            # Ensure .pdf extension
            if not save_path.endswith('.pdf'):
                save_path += '.pdf'
            
            # Perform merge
            output_file = self.pdf_service.merge_pdfs(files, save_path)
            
            logger.info(f"Merge successful: {output_file}")
            return {
                "success": True,
                "output": output_file,
                "message": f"Successfully merged {len(files)} PDFs"
            }
            
        except Exception as e:
            logger.error(f"Merge failed: {str(e)}")
            return {"success": False, "error": str(e)}

    def split_pdf(self, input_file, ranges, output_dir=None):
        """
        Split a PDF into multiple files.
        
        Args:
            input_file: Path to PDF to split
            ranges: List of page range strings (e.g., ["1-3", "4-6"])
            output_dir: Optional output directory
            
        Returns:
            dict: {"success": bool, "files": list, "error": str}
        """
        try:
            if not input_file:
                return {"success": False, "error": "No file selected"}
            
            if not ranges or len(ranges) == 0:
                return {"success": False, "error": "No page ranges specified"}
            
            # Ask user where to save split files
            if not output_dir:
                output_dir = self.window.create_file_dialog(
                    webview.FOLDER_DIALOG
                )
            
            # Handle different return types (string, list, tuple, or None)
            if output_dir is None:
                return {"success": False, "error": "Output folder selection cancelled"}
            elif isinstance(output_dir, (list, tuple)):
                output_dir = output_dir[0] if len(output_dir) > 0 else None
            
            if not output_dir:
                return {"success": False, "error": "No output folder selected"}
            
            # Perform split
            output_files = self.pdf_service.split_pdf(input_file, ranges, output_dir)
            
            logger.info(f"Split successful: {len(output_files)} files created")
            return {
                "success": True,
                "files": output_files,
                "message": f"Created {len(output_files)} PDF files"
            }
            
        except Exception as e:
            logger.error(f"Split failed: {str(e)}")
            return {"success": False, "error": str(e)}

    def compress_pdf(self, input_file, output_name=None):
        """
        Compress a PDF file.
        
        Args:
            input_file: Path to PDF to compress
            output_name: Optional output filename
            
        Returns:
            dict: {"success": bool, "output": str, "error": str}
        """
        try:
            if not input_file:
                return {"success": False, "error": "No file selected"}
            
            # Get original file size
            original_size = os.path.getsize(input_file)
            
            # Default output name
            if not output_name:
                base_name = os.path.splitext(os.path.basename(input_file))[0]
                output_name = f"{base_name}_compressed.pdf"
            
            # Ask user where to save
            save_path = self.window.create_file_dialog(
                webview.SAVE_DIALOG,
                save_filename=output_name,
                file_types=('PDF Files (*.pdf)',)
            )
            
            if not save_path:
                return {"success": False, "error": "Save cancelled"}
            
            # Ensure .pdf extension
            if not save_path.endswith('.pdf'):
                save_path += '.pdf'
            
            # Perform compression
            output_file = self.pdf_service.compress_pdf(input_file, save_path)
            
            # Get compressed file size
            compressed_size = os.path.getsize(output_file)
            reduction = ((original_size - compressed_size) / original_size) * 100
            
            logger.info(f"Compression successful: {reduction:.1f}% reduction")
            return {
                "success": True,
                "output": output_file,
                "original_size": original_size,
                "compressed_size": compressed_size,
                "reduction_percent": round(reduction, 1),
                "message": f"PDF compressed successfully"
            }
            
        except Exception as e:
            logger.error(f"Compression failed: {str(e)}")
            return {"success": False, "error": str(e)}

    def image_to_pdf(self, image_files, output_name=None):
        """
        Convert images to PDF.
        
        Args:
            image_files: List of image file paths
            output_name: Optional output filename
            
        Returns:
            dict: {"success": bool, "output": str, "error": str}
        """
        try:
            if not image_files or len(image_files) == 0:
                return {"success": False, "error": "No images selected"}
            
            # Default output name
            if not output_name:
                output_name = "images.pdf"
            
            # Ask user where to save
            save_path = self.window.create_file_dialog(
                webview.SAVE_DIALOG,
                save_filename=output_name,
                file_types=('PDF Files (*.pdf)',)
            )
            
            if not save_path:
                return {"success": False, "error": "Save cancelled"}
            
            # Ensure .pdf extension
            if not save_path.endswith('.pdf'):
                save_path += '.pdf'
            
            # Perform conversion
            output_file = self.pdf_service.image_to_pdf(image_files, save_path)
            
            logger.info(f"Image to PDF conversion successful")
            return {
                "success": True,
                "output": output_file,
                "message": f"Converted {len(image_files)} images to PDF"
            }
            
        except Exception as e:
            logger.error(f"Image to PDF conversion failed: {str(e)}")
            return {"success": False, "error": str(e)}

    def pdf_to_text(self, input_file):
        """
        Extract text from PDF.
        
        Args:
            input_file: Path to PDF file
            
        Returns:
            dict: {"success": bool, "text": str, "error": str}
        """
        try:
            if not input_file:
                return {"success": False, "error": "No file selected"}
            
            # Extract text
            text = self.pdf_service.pdf_to_text(input_file)
            
            logger.info(f"Text extraction successful")
            return {
                "success": True,
                "text": text,
                "message": "Text extracted successfully"
            }
            
        except Exception as e:
            logger.error(f"Text extraction failed: {str(e)}")
            return {"success": False, "error": str(e)}

    def select_files(self, file_types=None, multiple=True):
        """
        Open native file picker dialog.
        
        Args:
            file_types: Tuple of file type filters (e.g., ('PDF Files (*.pdf)', 'All Files (*.*)'))
            multiple: Allow multiple file selection
            
        Returns:
            List of selected file paths or None
        """
        try:
            if not file_types:
                file_types = ('PDF Files (*.pdf)',)
            
            dialog_type = webview.OPEN_DIALOG if multiple else webview.OPEN_DIALOG
            
            result = self.window.create_file_dialog(
                dialog_type,
                allow_multiple=multiple,
                file_types=file_types
            )
            
            # Handle different return types (list, tuple, or None)
            if result is None:
                return []
            elif isinstance(result, (list, tuple)):
                return list(result)  # Convert tuple to list
            else:
                return [result]  # Single file, wrap in list
            
        except Exception as e:
            logger.error(f"File selection failed: {str(e)}")
            return []

    def select_images(self, multiple=True):
        """
        Open file picker for image files.
        
        Args:
            multiple: Allow multiple file selection
            
        Returns:
            List of selected image file paths or None
        """
        file_types = (
            'Image Files (*.jpg;*.jpeg;*.png;*.bmp;*.gif;*.tiff)',
            'All Files (*.*)'
        )
        return self.select_files(file_types, multiple)

    def select_folder(self):
        """
        Open native folder picker dialog.
        
        Returns:
            Selected folder path or None
        """
        try:
            result = self.window.create_file_dialog(webview.FOLDER_DIALOG)
            # Handle list/tuple return on some platforms
            if isinstance(result, (list, tuple)):
                return result[0] if len(result) > 0 else None
            return result
        except Exception as e:
            logger.error(f"Folder selection failed: {str(e)}")
            return None

    def get_pdf_info(self, input_file):
        """
        Get information about a PDF file.
        
        Args:
            input_file: Path to PDF file
            
        Returns:
            dict: {"success": bool, "page_count": int, "error": str}
        """
        try:
            if not input_file:
                return {"success": False, "error": "No file provided"}
            
            from PyPDF2 import PdfReader
            reader = PdfReader(input_file)
            page_count = len(reader.pages)
            
            logger.info(f"PDF info: {page_count} pages")
            return {
                "success": True,
                "page_count": page_count,
                "file_size": os.path.getsize(input_file)
            }
            
        except Exception as e:
            logger.error(f"Get PDF info failed: {str(e)}")
            return {"success": False, "error": str(e)}

    def get_pdf_data(self, input_file):
        """
        Get PDF file data as base64 for frontend rendering.
        
        Args:
            input_file: Path to PDF file
            
        Returns:
            dict: {"success": bool, "data": str (base64), "error": str}
        """
        try:
            if not input_file:
                return {"success": False, "error": "No file provided"}
            
            import base64
            with open(input_file, 'rb') as f:
                pdf_data = f.read()
                base64_data = base64.b64encode(pdf_data).decode('utf-8')
            
            logger.info(f"PDF data loaded: {len(base64_data)} bytes (base64)")
            return {
                "success": True,
                "data": base64_data
            }
            
        except Exception as e:
            logger.error(f"Get PDF data failed: {str(e)}")
            return {"success": False, "error": str(e)}

    def navigate(self, page):
        """
        Navigate to a different page.
        
        Args:
            page: Page name (e.g., 'index', 'merge', 'split', etc.)
        """
        try:
            page_file = f"{page}.html"
            page_path = UI_DIR / page_file
            
            if page_path.exists():
                logger.info(f"Navigating to: {page}")
                self.window.load_url(str(page_path))
            else:
                logger.error(f"Page not found: {page_file}")
                
        except Exception as e:
            logger.error(f"Navigation failed: {str(e)}")

    def save_text_file(self, text, default_name="output.txt"):
        """
        Save text to a file using native save dialog.
        
        Args:
            text: Text content to save
            default_name: Default filename
            
        Returns:
            dict: {"success": bool, "path": str, "error": str}
        """
        try:
            save_path = self.window.create_file_dialog(
                webview.SAVE_DIALOG,
                save_filename=default_name,
                file_types=('Text Files (*.txt)', 'All Files (*.*)')
            )
            
            if not save_path:
                return {"success": False, "error": "Save cancelled"}
            
            # Ensure .txt extension
            if not save_path.endswith('.txt'):
                save_path += '.txt'
            
            # Write file
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(text)
            
            logger.info(f"Text saved to: {save_path}")
            return {"success": True, "path": save_path}
            
        except Exception as e:
            logger.error(f"Save failed: {str(e)}")
            return {"success": False, "error": str(e)}


def main():
    """Main application entry point."""
    
    # Create API instance
    api = Api()
    
    # Path to main HTML file
    index_path = str(UI_DIR / 'index.html')
    
    if not os.path.exists(index_path):
        logger.error(f"UI file not found: {index_path}")
        logger.error("Please ensure the ui/index.html file exists")
        return
    
    logger.info(f"Starting PDF Hub...")
    logger.info(f"Loading UI from: {index_path}")
    
    # Create window
    window = webview.create_window(
        title='PDF Hub',
        url=index_path,
        js_api=api,
        width=1200,
        height=800,
        resizable=True,
        background_color='#101622'
    )
    
    # Set window reference in API
    api.set_window(window)
    
    # Start the application
    webview.start(debug=True)


if __name__ == '__main__':
    main()
