from pathlib import Path

from app.infrastructure.parsers.strategies.docx_parser import DOCXParser

# Test function for DOCXParser
def test_docx_parser():
    parser = DOCXParser()

    try :
        sample_file = (
            Path(__file__).parent / "assets" / "Omar_Fadlallah_AI_Engineer_v13.docx"
        )
    except Exception as e:
        print(f"Error locating sample file: {e}")
        return

    text = parser.parse(str(sample_file))

    # print(text) 

    assert text.strip() != ""

test_docx_parser()

print("DOCXParser test passed successfully.")
# -------------------------------------------------

from app.infrastructure.parsers.strategies.pdf_parser import PDFParser

# Test function for PDFParser
def test_pdf_parser():
    parser = PDFParser()

    try :
        sample_file = (
            Path(__file__).parent / "assets" / "Omar_Fadlallah_AI_Engineer_v13.pdf"
        )
    except Exception as e:
        print(f"Error locating sample file: {e}")
        return

    text = parser.parse(str(sample_file))

    # print(text) 

    assert text.strip() != ""

test_pdf_parser()

print("PDFParser test passed successfully.")
# -------------------------------------------------


# -------------------------------------------------

from app.infrastructure.parsers.strategies.image_parser import ImageParser

# Test function for ImageParser
def test_image_parser():
    parser = ImageParser()

    try :
        sample_file = (
            Path(__file__).parent / "assets" / "Omar_Fadlallah_AI_Engineer_v13.pdf"
        )
    except Exception as e:
        print(f"Error locating sample file: {e}")
        return

    text = parser.parse(str(sample_file))

    # print(text) 

    assert text.strip() != ""

test_image_parser()

print("ImageParser test passed successfully.")
# -------------------------------------------------