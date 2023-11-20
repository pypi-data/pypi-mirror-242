try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

def image_to_text(image_path):
    """Convert image to text using Tesseract"""
    text = pytesseract.image_to_string(Image.open(image_path))
    return text

if __name__ == "__main__":
    # Example usage:
    image_path = input("Enter the path to the image: ")
    print(image_to_text(image_path))
