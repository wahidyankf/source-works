#!/usr/bin/env python3

import os
import re
import sys
import json
import tempfile
import argparse
import textwrap
import subprocess
from pathlib import Path
from typing import List, Tuple, Optional
from pypdf import PdfReader, PdfWriter, PdfMerger
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import black, blue
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import Paragraph, SimpleDocTemplate, Frame


def create_toc_page(filenames: list[str], page_numbers: list[int]) -> str:
    """Create a table of contents pages and return the path."""
    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    temp_path = temp_file.name
    temp_file.close()
    
    can = canvas.Canvas(temp_path, pagesize=letter)
    width, height = letter
    
    # Constants for layout
    title_font_size = 24
    text_font_size = 12
    line_height = 20  # Standard line height
    margin_left = 72  # Left margin
    margin_right = 72  # Right margin
    dot_spacing = 4  # Space between dots
    page_number_width = 40  # Width reserved for page number
    indent = 20  # Indentation for wrapped lines
    max_text_width = width - margin_left - margin_right - page_number_width - 50  # Maximum width for text
    top_margin = 72  # Top margin
    bottom_margin = 72  # Bottom margin
    
    def format_display_name(filename: str) -> str:
        """Format the filename for display in TOC."""
        # Remove extension
        name = os.path.splitext(filename)[0]
        return name
    
    def wrap_text(text: str, max_width: float) -> list[str]:
        """Wrap text to fit within max_width."""
        words = text.split()
        lines = []
        current_line = []
        current_width = 0
        
        for word in words:
            word_width = stringWidth(word, "Helvetica", 12)
            space_width = stringWidth(" ", "Helvetica", 12) if current_line else 0
            
            if current_width + word_width + space_width <= max_width:
                current_line.append(word)
                current_width += word_width + space_width
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]
                current_width = word_width
        
        if current_line:
            lines.append(" ".join(current_line))
        
        return lines
    
    def draw_title(y: float) -> float:
        """Draw the title and return the new y position."""
        can.setFont("Helvetica-Bold", title_font_size)
        title = "Table of Contents"
        title_width = stringWidth(title, "Helvetica-Bold", title_font_size)
        can.drawString((width - title_width) / 2, y, title)
        return y - (title_font_size + line_height)
    
    def start_new_page() -> float:
        """Start a new page and return the starting y position."""
        can.showPage()
        can.setFont("Helvetica", text_font_size)
        return height - top_margin
    
    # Start drawing TOC
    y = height - top_margin
    y = draw_title(y) - line_height  # Account for title and extra spacing
    
    # Draw entries
    can.setFont("Helvetica", text_font_size)
    for filename, page_num in zip(filenames, page_numbers):
        display_text = format_display_name(filename)
        lines = wrap_text(display_text, max_text_width)
        
        # Check if we need a new page
        if y - (len(lines) * line_height) < bottom_margin:
            y = start_new_page()
        
        # Draw first line with dots and page number
        first_line = lines[0]
        text_width = stringWidth(first_line, "Helvetica", text_font_size)
        can.drawString(margin_left, y, first_line)
        
        # Draw dots
        dots_width = width - margin_left - margin_right - text_width - page_number_width
        num_dots = int(dots_width / dot_spacing)
        dots_y = y + text_font_size / 4  # Adjust dot position to align with text
        for i in range(num_dots):
            can.drawString(margin_left + text_width + (i * dot_spacing), y, ".")
        
        # Draw page number
        page_num_str = str(page_num)
        page_num_width = stringWidth(page_num_str, "Helvetica", text_font_size)
        can.drawString(width - margin_right - page_num_width, y, page_num_str)
        
        y -= line_height
        
        # Draw remaining lines if any
        for line in lines[1:]:
            # Check if we need a new page
            if y < bottom_margin:
                y = start_new_page()
            can.drawString(margin_left + indent, y, line)
            y -= line_height
    
    can.save()
    return temp_path


def create_title_page(filename: str) -> str:
    """Create a PDF page with the filename as its content."""
    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    temp_path = temp_file.name
    temp_file.close()

    # Create the PDF
    c = canvas.Canvas(temp_path, pagesize=letter)
    width, height = letter

    # Set margins to 10% of page width
    margin = width * 0.1
    max_width = width - (2 * margin)

    # Start with a large font size and reduce if necessary
    font_name = "Helvetica"
    font_size = 24
    c.setFont(font_name, font_size)
    text_width = stringWidth(filename, font_name, font_size)

    # Reduce font size until text fits within margins
    while text_width > max_width and font_size > 12:
        font_size -= 1
        c.setFont(font_name, font_size)
        text_width = stringWidth(filename, font_name, font_size)

    # Center the text
    x = (width - text_width) / 2
    y = (height + font_size) / 2

    # Draw the text
    c.setFillColor(black)
    c.drawString(x, y, filename)
    c.showPage()
    c.save()

    return temp_path


def get_unique_filename(directory: Path, base_name: str) -> str:
    """Generate a unique filename in the given directory."""
    if not os.path.exists(directory / base_name):
        return base_name

    base, ext = os.path.splitext(base_name)
    counter = 1
    while os.path.exists(directory / f"{base}_{counter}{ext}"):
        counter += 1
    return f"{base}_{counter}{ext}"


def add_page_numbers(input_path: str, output_path: str, total_pages: int):
    """Add page numbers to the bottom of each page."""
    reader = PdfReader(input_path)
    writer = PdfWriter()
    
    # Add pages with page numbers
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        
        # Create a canvas for the page number
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        
        # Add page number at the bottom center
        can.drawString(letter[0]/2 - 20, 30, f"Page {page_num + 1} of {total_pages}")
        can.save()
        
        # Move to the beginning of the StringIO buffer
        packet.seek(0)
        new_pdf = PdfReader(packet)
        
        # Merge the page number with the existing page
        page.merge_page(new_pdf.pages[0])
        writer.add_page(page)
    
    # Copy bookmarks
    for bookmark in reader.outline:
        if isinstance(bookmark, dict):
            # This is a bookmark dictionary
            writer.add_outline_item(
                bookmark.get('/Title', ''),
                bookmark.get('/Page', 0)
            )
    
    # Write the result to a temporary file
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)


def merge_pdfs(input_dir: Path, output_name: str = "merged_pdfs.pdf") -> None:
    """
    Merge all PDFs in the input directory into a single PDF with a table of contents.
    """
    # Get list of PDF files
    pdf_files = sorted([f for f in input_dir.glob("*.pdf") if f.name != output_name and not f.name.startswith('merged_pdfs')])
    
    if not pdf_files:
        print("No PDF files found to merge")
        return
    
    # Get page counts for each PDF
    page_counts = []
    for pdf_file in pdf_files:
        with open(pdf_file, 'rb') as file:
            pdf = PdfReader(file)
            page_counts.append(len(pdf.pages))
    print(f"PDF page counts: {page_counts}")
    
    # Calculate actual page numbers for TOC
    page_numbers = []
    
    # First document starts at page 4 (after TOC)
    current_page = 4
    page_numbers.append(current_page)
    
    # Calculate remaining page numbers
    for i in range(1, len(pdf_files)):
        # Add previous document's pages + 1 for title page
        current_page += page_counts[i-1] + 1
        page_numbers.append(current_page)
    
    print(f"Final page numbers: {page_numbers}")
    
    # Create TOC with correct page numbers
    toc_path = create_toc_page([f.name for f in pdf_files], page_numbers)
    
    # Create writer object
    writer = PdfWriter()
    
    # Add TOC to the beginning
    with open(toc_path, 'rb') as file:
        toc_reader = PdfReader(file)
        for page in toc_reader.pages:
            writer.add_page(page)
    
    # Add all PDF files with their title pages
    current_page = len(writer.pages)  # Start after TOC pages
    
    for i, pdf_file in enumerate(pdf_files):
        # Add title page
        title_path = create_title_page(pdf_file.name)
        with open(title_path, 'rb') as file:
            title_reader = PdfReader(file)
            for page in title_reader.pages:
                writer.add_page(page)
                current_page += 1
            
            # Add bookmark for the document
            writer.add_outline_item(pdf_file.name, current_page - 1)  # -1 because current_page is next page
        
        # Add actual PDF content
        with open(pdf_file, 'rb') as file:
            pdf_reader = PdfReader(file)
            for page in pdf_reader.pages:
                writer.add_page(page)
                current_page += 1
        
        # Clean up title page
        os.unlink(title_path)
    
    # Create output directory if it doesn't exist
    output_path = input_dir / output_name
    if output_path.exists():
        output_name = get_unique_filename(input_dir, output_name)
        output_path = input_dir / output_name
    
    # Write merged PDF to a temporary file first
    temp_output = str(output_path) + ".temp"
    print(f"Writing merged PDF to: {output_path}")
    with open(temp_output, 'wb') as output_file:
        writer.write(output_file)
    
    # Calculate total pages
    with open(temp_output, 'rb') as file:
        pdf = PdfReader(file)
        total_pages = len(pdf.pages)
    
    # Add page numbers
    add_page_numbers(temp_output, str(output_path), total_pages)
    
    # Clean up
    os.unlink(toc_path)
    os.unlink(temp_output)
    
    print("PDF merge complete!")


def main():
    parser = argparse.ArgumentParser(description="PDF Merger Tool")
    parser.add_argument("--merge-pdf", action="store_true", help="Merge PDF files")
    parser.add_argument(
        "-dir", "--directory", type=str, help="Directory containing PDF files"
    )
    parser.add_argument(
        "-n",
        "--name",
        type=str,
        default="merged_pdfs.pdf",
        help="Output filename (default: merged_pdfs.pdf)",
    )

    args = parser.parse_args()

    if args.merge_pdf:
        if not args.directory:
            print("Error: Please specify a directory using -dir or --directory")
            return

        # Convert directory to absolute path if it's relative
        directory = Path(args.directory).resolve()

        if not directory.exists():
            print(f"Error: Directory does not exist: {directory}")
            return

        if not directory.is_dir():
            print(f"Error: Not a directory: {directory}")
            return

        merge_pdfs(directory, args.name)


if __name__ == "__main__":
    main()
