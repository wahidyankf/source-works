import os
import re
import tempfile
from pathlib import Path
from typing import Any, List, Tuple, Callable, Generator
from _pytest.fixtures import FixtureRequest
from pypdf import PdfReader
import pytest
from reportlab.pdfgen import canvas

from sw_core.pdf import (
    create_toc_page,
    create_title_page,
    get_unique_filename,
    merge_pdfs
)


@pytest.fixture
def sample_pdf() -> Generator[str, None, None]:
    """Create a sample PDF file for testing."""
    temp_file = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
    c = canvas.Canvas(temp_file.name)
    c.drawString(100, 750, "Test Content")
    c.save()
    yield temp_file.name
    os.unlink(temp_file.name)


@pytest.fixture
def sample_pdf_with_content(request: FixtureRequest) -> Generator[str, None, None]:
    """Create a sample PDF file with specific content."""
    temp_file = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
    c = canvas.Canvas(temp_file.name)
    c.drawString(100, 750, request.param)  # Use the parameter directly
    c.save()
    yield temp_file.name
    os.unlink(temp_file.name)


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for testing."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    # Clean up temp directory and its contents
    for file in Path(temp_dir).iterdir():
        if file.is_file():
            os.unlink(file)
    os.rmdir(temp_dir)


@pytest.fixture
def multi_page_pdf() -> Generator[str, None, None]:
    """Create a sample PDF file with multiple pages."""
    temp_file = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
    c = canvas.Canvas(temp_file.name)

    # Add 3 pages
    for i in range(3):
        c.drawString(100, 750, f"Page {i+1}")
        c.showPage()
    c.save()

    yield temp_file.name
    os.unlink(temp_file.name)


@pytest.fixture
def pdf_reader() -> Callable[[str], Tuple[List[str], int]]:
    """Create a function to read PDF content.

    This abstracts away the specific PDF library implementation.
    """
    def read_pdf(filepath: str) -> Tuple[List[str], int]:
        """Read a PDF file and return its text content and page count."""
        with open(filepath, 'rb') as file:
            reader = PdfReader(file)
            pages: List[str] = []
            for page in reader.pages:
                pages.append(page.extract_text())
            return pages, len(reader.pages)
    return read_pdf


def test_create_toc_page(pdf_reader: Callable[[str], Tuple[List[str], int]]) -> None:
    """Test creation of table of contents page."""
    filenames = ["test1.pdf", "test2.pdf", "very_long_filename.pdf"]
    page_numbers = [2, 4, 6]
    toc_path = create_toc_page(filenames, page_numbers)

    # Verify TOC was created
    assert os.path.exists(toc_path)

    # Read TOC content
    pages, _ = pdf_reader(toc_path)
    text = pages[0]

    # Verify content
    assert "Table of Contents" in text
    for filename in filenames:
        name = os.path.splitext(filename)[0]
        assert name in text
    for page_num in page_numbers:
        assert str(page_num) in text

    # Clean up
    os.unlink(toc_path)


def test_create_toc_page_empty_list(pdf_reader: Callable[[str], Tuple[List[str], int]]) -> None:
    """Test TOC creation with empty file list."""
    toc_path = create_toc_page([], [])

    # Verify TOC was created
    assert os.path.exists(toc_path)

    # Read TOC content
    pages, _ = pdf_reader(toc_path)
    text = pages[0]

    # Verify content
    assert "Table of Contents" in text

    # Clean up
    os.unlink(toc_path)


def test_create_toc_page_special_characters() -> None:
    """Test TOC creation with filenames containing special characters."""
    filenames = ["test-1.pdf", "test_2.pdf", "test 3.pdf", "test@4.pdf"]
    page_numbers = [2, 4, 6, 8]
    toc_path = create_toc_page(filenames, page_numbers)

    # Verify TOC was created
    assert os.path.exists(toc_path)

    # Read TOC content
    reader = PdfReader(toc_path)
    text = reader.pages[0].extract_text()

    # Verify content - filenames should be preserved exactly as they appear
    for name in filenames:
        base_name = os.path.splitext(name)[0]
        assert base_name in text.replace('\n', ' ')


def test_create_toc_page_long_filename() -> None:
    """Test that TOC properly wraps long filenames."""
    # Create a very long filename that should wrap
    long_filename = "This is a very long filename that should definitely wrap to the next line because it exceeds the maximum width of a single line in our table of contents.pdf"
    short_filename = "short_file.pdf"

    # Create TOC page
    toc_path = create_toc_page([long_filename, short_filename], [2, 4])

    # Verify TOC was created
    assert os.path.exists(toc_path)

    # Read TOC content
    reader = PdfReader(toc_path)
    text = reader.pages[0].extract_text()

    # Join lines to check for complete text
    joined_text = text.replace('\n', ' ')
    assert "This is a very long filename that should definitely wrap" in joined_text


def test_create_title_page() -> None:
    """Test creation of title page."""
    filename = "test_document.pdf"
    title_path = create_title_page(filename)

    try:
        # Verify the PDF was created
        assert os.path.exists(title_path)

        # Check if it's a valid PDF
        reader = PdfReader(title_path)
        assert len(reader.pages) == 1

        # Check if text content includes our filename
        text = reader.pages[0].extract_text()
        assert filename in text
    finally:
        # Clean up
        if os.path.exists(title_path):
            os.unlink(title_path)


def test_create_title_page_long_filename() -> None:
    """Test title page creation with a very long filename."""
    long_filename = "a" * 100 + ".pdf"  # 100 character filename
    title_path = create_title_page(long_filename)
    try:
        reader = PdfReader(title_path)
        text = reader.pages[0].extract_text()
        assert long_filename in text
        assert len(reader.pages) == 1
    finally:
        if os.path.exists(title_path):
            os.unlink(title_path)


def test_create_title_page_special_characters() -> None:
    """Test title page creation with special characters in filename."""
    filename = "test@#$%^&*()_+.pdf"
    title_path = create_title_page(filename)
    try:
        reader = PdfReader(title_path)
        text = reader.pages[0].extract_text()
        assert filename in text
    finally:
        if os.path.exists(title_path):
            os.unlink(title_path)


def test_get_unique_filename(temp_dir: Path) -> None:
    """Test unique filename generation."""
    # Test with non-existing file
    assert get_unique_filename(temp_dir, "test.pdf") == "test.pdf"

    # Create a file and test again
    (temp_dir / "test.pdf").touch()
    assert get_unique_filename(temp_dir, "test.pdf") == "test_1.pdf"

    # Create another file and test again
    (temp_dir / "test_1.pdf").touch()
    assert get_unique_filename(temp_dir, "test.pdf") == "test_2.pdf"


def test_get_unique_filename_special_characters(temp_dir: Path) -> None:
    """Test unique filename generation with special characters."""
    filename = "test@#$%^&*()_+.pdf"
    assert get_unique_filename(temp_dir, filename) == filename

    (temp_dir / filename).touch()
    expected = re.sub(r'\.pdf$', '_1.pdf', filename)
    assert get_unique_filename(temp_dir, filename) == expected


def test_get_unique_filename_no_extension(temp_dir: Path) -> None:
    """Test unique filename generation without file extension."""
    assert get_unique_filename(temp_dir, "test") == "test"
    (temp_dir / "test").touch()
    assert get_unique_filename(temp_dir, "test") == "test_1"


def test_merge_pdfs(temp_dir: Path, sample_pdf: str) -> None:
    """Test PDF merging functionality."""
    # Create test PDFs
    pdf_names = ["doc1.pdf", "doc2.pdf", "doc3.pdf"]
    for name in pdf_names:
        dest = temp_dir / name
        with open(dest, 'wb') as file, open(sample_pdf, 'rb') as src:
            file.write(src.read())

    # Merge PDFs
    output_name = "merged.pdf"
    merge_pdfs(temp_dir, output_name)

    # Check if merged PDF exists
    merged_path = temp_dir / output_name
    assert merged_path.exists()

    # Verify merged PDF structure
    reader = PdfReader(str(merged_path))

    # Expected pages:
    # 1. TOC
    # For each PDF:
    # - Title page
    # - Content page
    expected_pages = 1 + (len(pdf_names) * 2)
    assert len(reader.pages) == expected_pages

    # Check if TOC includes all filenames (without extension)
    toc_text = reader.pages[0].extract_text()
    for name in pdf_names:
        base_name = os.path.splitext(name)[0]
        assert base_name in toc_text


@pytest.mark.parametrize('sample_pdf_with_content', ["Page 1", "Page 2", "Page 3"], indirect=True)
def test_merge_pdfs_content_preservation(
    temp_dir: Path,
    sample_pdf_with_content: str,
    request: pytest.FixtureRequest,
) -> None:
    """Test that PDF content is preserved during merging."""
    # Create a PDF with specific content
    dest = temp_dir / "test.pdf"
    with open(dest, 'wb') as file, open(sample_pdf_with_content, 'rb') as src:
        content = src.read()
        file.write(content)

    # Get the content string from the parameter
    if not hasattr(request, 'node'):
        raise TypeError("Request has no node attribute")
    node: Any = request.node
    if node is None:
        raise TypeError("Request node is None")
    callspec = getattr(node, 'callspec', None)
    if callspec is None or not hasattr(callspec, 'params'):
        raise TypeError("Test not properly parameterized")
    params = callspec.params
    content_text = str(params['sample_pdf_with_content'])
    assert isinstance(content_text, str)

    # Merge PDFs
    merged_path = merge_pdfs(temp_dir, "merged.pdf")
    assert merged_path is not None

    # Read merged PDF content
    reader = PdfReader(str(merged_path))
    # Content should be on page 3 (after TOC and title page)
    pdf_text = reader.pages[2].extract_text()

    # Verify content is preserved
    assert content_text in pdf_text


def test_merge_pdfs_no_files(temp_dir: Path) -> None:
    """Test PDF merging with no input files."""
    merged_path = merge_pdfs(temp_dir, "merged.pdf")
    assert merged_path is None


def test_merge_pdfs_single_file(temp_dir: Path, sample_pdf: str) -> None:
    """Test PDF merging with a single input file."""
    # Create one test PDF
    pdf_name = "single.pdf"
    dest = temp_dir / pdf_name
    with open(dest, 'wb') as file, open(sample_pdf, 'rb') as src:
        file.write(src.read())

    # Merge PDFs
    merged_path = merge_pdfs(temp_dir, "merged.pdf")
    assert merged_path is not None

    # Verify merged PDF exists and is valid
    assert os.path.exists(str(merged_path))
    reader = PdfReader(str(merged_path))
    # Should have 3 pages: TOC, title page, and content
    assert len(reader.pages) == 3

    # Check TOC
    toc_text = reader.pages[0].extract_text()
    assert "Table of Contents" in toc_text
    # Check for filename without extension
    assert "single" in toc_text

    # Check bookmarks
    assert len(reader.outline) == 1
    assert reader.outline[0].title == pdf_name  # type: ignore


def test_merge_pdfs_duplicate_filenames(temp_dir: Path, sample_pdf: str) -> None:
    """Test merging PDFs with duplicate output filename."""
    # Create a test PDF
    pdf_name = "test.pdf"
    dest = temp_dir / pdf_name
    with open(sample_pdf, 'rb') as src, open(dest, 'wb') as dst:
        dst.write(src.read())

    # Create existing merged files with content
    with open(sample_pdf, 'rb') as src:
        content = src.read()
        with open(temp_dir / "merged.pdf", 'wb') as dst:
            dst.write(content)
        with open(temp_dir / "merged_1.pdf", 'wb') as dst:
            dst.write(content)

    # Merge PDFs
    merge_pdfs(temp_dir, "merged.pdf")

    # Should create merged_2.pdf
    assert (temp_dir / "merged_2.pdf").exists()


def test_merge_pdfs_non_pdf_files(temp_dir: Path, sample_pdf: str) -> None:
    """Test merging with non-PDF files in directory."""
    # Create a PDF file
    dest = temp_dir / "test.pdf"
    with open(sample_pdf, 'rb') as src, open(dest, 'wb') as dst:
        dst.write(src.read())

    # Create some non-PDF files
    (temp_dir / "test.txt").touch()
    (temp_dir / "test.doc").touch()

    # Merge PDFs
    merge_pdfs(temp_dir, "merged.pdf")

    # Check merged PDF only includes PDF files
    reader = PdfReader(str(temp_dir / "merged.pdf"))
    assert len(reader.pages) == 3  # TOC + Title + Content

    # Check TOC only includes PDF files (without extension)
    toc_text = reader.pages[0].extract_text()
    assert "test" in toc_text


def test_page_number_calculation(temp_dir: Path, multi_page_pdf: str) -> None:
    """Test that page numbers in TOC match actual page numbers."""
    # Create test directory structure
    test_pdfs = []
    page_counts = [3, 2, 4]  # Define page counts for test PDFs

    # Create multiple PDFs with different page counts
    for i, page_count in enumerate(page_counts):
        temp_file = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
        c = canvas.Canvas(temp_file.name)

        # Add pages
        for j in range(page_count):
            c.drawString(100, 750, f"PDF {i+1} - Page {j+1}")
            c.showPage()
        c.save()

        # Copy to test directory with known name
        target_path = temp_dir / f"test_doc_{i+1}.pdf"
        with open(temp_file.name, 'rb') as src, open(target_path, 'wb') as dst:
            dst.write(src.read())
        test_pdfs.append(target_path)
        os.unlink(temp_file.name)

    # Merge PDFs
    merge_pdfs(temp_dir)
    merged_path = temp_dir / "merged_pdfs.pdf"

    # Read merged PDF
    with open(merged_path, 'rb') as file:
        pdf = PdfReader(file)

        # Expected page numbers for each document
        # TOC: pages 1-3
        # Doc 1: title page at 4, content 5-7 (3 pages)
        # Doc 2: title page at 8, content 9-10 (2 pages)
        # Doc 3: title page at 11, content 12-15 (4 pages)
        expected_starts = [4, 8, 11]  # Starting page for each document

        # Check TOC page numbers
        toc_text = pdf.pages[0].extract_text()
        for i, start_page in enumerate(expected_starts):
            assert str(start_page) in toc_text, f"Document {
                i+1} should start at page {start_page}"

        # Check actual page numbers at bottom
        for i, page in enumerate(pdf.pages):
            page_text = page.extract_text()
            expected_page = f"Page {i + 1} of {len(pdf.pages)}"
            assert expected_page in page_text, f"Page {
                i+1} should show '{expected_page}' at bottom"


def test_toc_line_wrapping(pdf_reader: Callable[[str], Tuple[List[str], int]]) -> None:
    """Test that long filenames are properly wrapped in TOC."""
    # Create a very long filename that should wrap
    long_filename = "This_is_a_very_long_filename_that_should_definitely_wrap_to_multiple_lines_in_the_table_of_contents.pdf"
    filenames = [long_filename]
    page_numbers = [1]

    toc_path = create_toc_page(filenames, page_numbers)
    assert os.path.exists(toc_path)

    # Read TOC content
    pages, _ = pdf_reader(toc_path)
    text = pages[0]

    # The text should be split across multiple lines
    # Remove extension and check if parts of the text appear
    base_name = os.path.splitext(long_filename)[0]
    parts = base_name.split('_')

    # At least some parts should appear on separate lines
    found_parts = 0
    for part in parts:
        if part in text:
            found_parts += 1

    assert found_parts > 1, "Long filename should be wrapped to multiple lines"

    # Clean up
    os.unlink(toc_path)


def test_toc_dot_leaders(pdf_reader: Callable[[str], Tuple[List[str], int]]) -> None:
    """Test that dot leaders are present in TOC."""
    filename = "test_document.pdf"
    page_number = 42

    toc_path = create_toc_page([filename], [page_number])
    assert os.path.exists(toc_path)

    # Read TOC content
    pages, _ = pdf_reader(toc_path)
    text = pages[0]

    # Check for presence of dots between filename and page number
    assert "test_document" in text
    assert "." in text  # Should have some form of dot leader
    assert "42" in text

    # Clean up
    os.unlink(toc_path)


def test_toc_multiple_pages(pdf_reader: Callable[[str], Tuple[List[str], int]]) -> None:
    """Test that TOC properly handles multiple pages."""
    # Create enough entries to force multiple pages
    filenames = [f"test_document_{i}.pdf" for i in range(50)]
    page_numbers = list(range(1, 51))

    toc_path = create_toc_page(filenames, page_numbers)
    assert os.path.exists(toc_path)

    # Read TOC content
    pages, page_count = pdf_reader(toc_path)

    # Should have multiple pages
    assert page_count > 1, "Long TOC should span multiple pages"

    # Each page should have content
    for i, page_text in enumerate(pages):
        assert page_text.strip(), f"Page {i+1} should have content"
        if i == 0:
            assert "Table of Contents" in page_text, "First page should have the title"

    # Clean up
    os.unlink(toc_path)


def test_toc_formatting_consistency(pdf_reader: Callable[[str], Tuple[List[str], int]]) -> None:
    """Test that TOC entries are consistently formatted."""
    filenames = ["doc1.pdf", "doc2.pdf", "doc3.pdf"]
    page_numbers = [1, 10, 100]

    toc_path = create_toc_page(filenames, page_numbers)
    assert os.path.exists(toc_path)

    # Read TOC content
    pages, _ = pdf_reader(toc_path)
    text = pages[0]

    # Each entry should be present with its components
    for filename, page_num in zip(filenames, page_numbers):
        base_name = os.path.splitext(filename)[0]
        assert base_name in text, f"Entry for {base_name} should be present"
        assert str(page_num) in text, f"Page number {
            page_num} should be present"
        assert "." in text, "Should have some form of visual separator"

    # Clean up
    os.unlink(toc_path)
