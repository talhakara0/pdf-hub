"""
PDF Service Module
Provides PDF operations: merge, split, compress, image-to-PDF, and text extraction.
"""

import os
import logging
from typing import List
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from PIL import Image

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PdfService:
    """Service class for handling all PDF operations."""

    def merge_pdfs(self, input_files: List[str], output_file: str) -> str:
        """
        Merge multiple PDF files into a single PDF.
        
        Args:
            input_files: List of paths to PDF files to merge
            output_file: Path where the merged PDF will be saved
            
        Returns:
            Path to the merged PDF file
            
        Raises:
            FileNotFoundError: If any input file doesn't exist
            Exception: For any PDF processing errors
        """
        try:
            # Validate input files
            for file_path in input_files:
                if not os.path.exists(file_path):
                    raise FileNotFoundError(f"File not found: {file_path}")
            
            logger.info(f"Merging {len(input_files)} PDF files...")
            
            # Create merger object
            merger = PdfMerger()
            
            # Add each PDF
            for pdf_file in input_files:
                logger.info(f"Adding: {pdf_file}")
                merger.append(pdf_file)
            
            # Write merged PDF
            merger.write(output_file)
            merger.close()
            
            logger.info(f"Successfully merged PDFs to: {output_file}")
            return output_file
            
        except Exception as e:
            logger.error(f"Error merging PDFs: {str(e)}")
            raise

    def split_pdf(self, input_file: str, ranges: List[str], output_dir: str) -> List[str]:
        """
        Split a PDF into multiple files based on page ranges.
        
        Args:
            input_file: Path to the PDF file to split
            ranges: List of page ranges (e.g., ["1-3", "4-6", "7"])
            output_dir: Directory where split PDFs will be saved
            
        Returns:
            List of paths to the created PDF files
            
        Raises:
            FileNotFoundError: If input file doesn't exist
            ValueError: If page ranges are invalid
            Exception: For any PDF processing errors
        """
        try:
            # Validate input
            if not os.path.exists(input_file):
                raise FileNotFoundError(f"File not found: {input_file}")
            
            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            # Read the PDF
            reader = PdfReader(input_file)
            total_pages = len(reader.pages)
            
            logger.info(f"Splitting PDF with {total_pages} pages into {len(ranges)} parts...")
            
            output_files = []
            base_name = os.path.splitext(os.path.basename(input_file))[0]
            
            # Process each range
            for idx, page_range in enumerate(ranges, 1):
                # Parse the range
                pages = self._parse_page_range(page_range, total_pages)
                
                # Create new PDF for this range
                writer = PdfWriter()
                
                for page_num in pages:
                    writer.add_page(reader.pages[page_num - 1])  # Convert to 0-indexed
                
                # Generate output filename
                output_file = os.path.join(output_dir, f"{base_name}_part{idx}.pdf")
                
                # Write the split PDF
                with open(output_file, 'wb') as output:
                    writer.write(output)
                
                output_files.append(output_file)
                logger.info(f"Created: {output_file} (pages {page_range})")
            
            logger.info(f"Successfully split PDF into {len(output_files)} files")
            return output_files
            
        except Exception as e:
            logger.error(f"Error splitting PDF: {str(e)}")
            raise

    def _parse_page_range(self, page_range: str, total_pages: int) -> List[int]:
        """
        Parse a page range string into a list of page numbers.
        
        Args:
            page_range: String like "1-3,5,7-9"
            total_pages: Total number of pages in the PDF
            
        Returns:
            List of page numbers
            
        Raises:
            ValueError: If range is invalid
        """
        pages = []
        parts = page_range.replace(' ', '').split(',')
        
        for part in parts:
            if '-' in part:
                # Range like "1-3"
                start, end = part.split('-')
                start, end = int(start), int(end)
                
                if start < 1 or end > total_pages or start > end:
                    raise ValueError(f"Invalid range: {part} (PDF has {total_pages} pages)")
                
                pages.extend(range(start, end + 1))
            else:
                # Single page
                page = int(part)
                
                if page < 1 or page > total_pages:
                    raise ValueError(f"Invalid page: {page} (PDF has {total_pages} pages)")
                
                pages.append(page)
        
        return pages

    def compress_pdf(self, input_file: str, output_file: str) -> str:
        """
        Compress a PDF file by rewriting it.
        Note: This is a basic compression. For better results, image compression could be added.
        
        Args:
            input_file: Path to the PDF file to compress
            output_file: Path where compressed PDF will be saved
            
        Returns:
            Path to the compressed PDF file
            
        Raises:
            FileNotFoundError: If input file doesn't exist
            Exception: For any PDF processing errors
        """
        try:
            # Validate input
            if not os.path.exists(input_file):
                raise FileNotFoundError(f"File not found: {input_file}")
            
            logger.info(f"Compressing PDF: {input_file}")
            
            # Read the PDF
            reader = PdfReader(input_file)
            writer = PdfWriter()
            
            # Copy all pages
            for page in reader.pages:
                writer.add_page(page)
            
            # Write compressed PDF
            with open(output_file, 'wb') as output:
                writer.write(output)
            
            # Get file sizes
            original_size = os.path.getsize(input_file)
            compressed_size = os.path.getsize(output_file)
            reduction = ((original_size - compressed_size) / original_size) * 100
            
            logger.info(f"Compression complete. Size reduction: {reduction:.1f}%")
            logger.info(f"Original: {original_size / 1024:.2f} KB, Compressed: {compressed_size / 1024:.2f} KB")
            
            return output_file
            
        except Exception as e:
            logger.error(f"Error compressing PDF: {str(e)}")
            raise

    def image_to_pdf(self, image_files: List[str], output_file: str) -> str:
        """
        Convert multiple images to a single PDF file.
        
        Args:
            image_files: List of paths to image files (JPG, PNG, etc.)
            output_file: Path where the PDF will be saved
            
        Returns:
            Path to the created PDF file
            
        Raises:
            FileNotFoundError: If any image file doesn't exist
            Exception: For any image processing errors
        """
        try:
            # Validate input files
            for file_path in image_files:
                if not os.path.exists(file_path):
                    raise FileNotFoundError(f"File not found: {file_path}")
            
            logger.info(f"Converting {len(image_files)} images to PDF...")
            
            # Open all images
            images = []
            for image_file in image_files:
                img = Image.open(image_file)
                
                # Convert to RGB if necessary (for PNG with transparency, etc.)
                if img.mode in ('RGBA', 'LA', 'P'):
                    rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                    rgb_img.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                    img = rgb_img
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                images.append(img)
                logger.info(f"Loaded: {image_file}")
            
            # Save as PDF
            if images:
                images[0].save(output_file, 'PDF', save_all=True, append_images=images[1:])
                logger.info(f"Successfully created PDF: {output_file}")
            
            return output_file
            
        except Exception as e:
            logger.error(f"Error converting images to PDF: {str(e)}")
            raise

    def pdf_to_text(self, input_file: str) -> str:
        """
        Extract text from all pages of a PDF.
        
        Args:
            input_file: Path to the PDF file
            
        Returns:
            Extracted text as a string
            
        Raises:
            FileNotFoundError: If input file doesn't exist
            Exception: For any PDF processing errors
        """
        try:
            # Validate input
            if not os.path.exists(input_file):
                raise FileNotFoundError(f"File not found: {input_file}")
            
            logger.info(f"Extracting text from: {input_file}")
            
            # Read the PDF
            reader = PdfReader(input_file)
            total_pages = len(reader.pages)
            
            # Extract text from all pages
            text_content = []
            for page_num, page in enumerate(reader.pages, 1):
                text = page.extract_text()
                if text.strip():
                    text_content.append(f"=== Page {page_num} ===\n{text}\n")
                    logger.info(f"Extracted text from page {page_num}/{total_pages}")
            
            full_text = '\n'.join(text_content)
            logger.info(f"Successfully extracted text from {total_pages} pages")
            
            return full_text
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            raise
