"""
Document Processing Agent
Handles PDF and image text extraction
"""

import os
import pytesseract
from PIL import Image
from pypdf import PdfReader


def process_pdf(file_path: str) -> dict:
    """
    Extracts text from PDF file
    
    Args:
        file_path: Path to PDF file
        
    Returns:
        Dictionary with extracted text and metadata
    """
    try:
        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}", "text": ""}
        
        reader = PdfReader(file_path)
        text = ""
        
        for page_num, page in enumerate(reader.pages):
            page_text = page.extract_text()
            text += f"\n--- Page {page_num + 1} ---\n{page_text}"
        
        return {
            "file_path": file_path,
            "pages": len(reader.pages),
            "text": text,
            "success": True
        }
    
    except Exception as e:
        return {
            "error": str(e),
            "file_path": file_path,
            "text": "",
            "success": False
        }


def process_image(file_path: str, language: str = 'eng+hin') -> dict:
    """
    Extracts text from image using OCR
    
    Args:
        file_path: Path to image file
        language: Tesseract language code (default: English + Hindi)
        
    Returns:
        Dictionary with extracted text and metadata
    """
    try:
        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}", "text": ""}
        
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img, lang=language)
        
        return {
            "file_path": file_path,
            "image_size": img.size,
            "text": text,
            "success": True
        }
    
    except Exception as e:
        return {
            "error": str(e),
            "file_path": file_path,
            "text": "",
            "success": False
        }


def process_resume(file_path: str) -> dict:
    """
    Processes resume (PDF or image) and extracts relevant information
    
    Args:
        file_path: Path to resume file
        
    Returns:
        Extracted resume information
    """
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if file_ext == '.pdf':
        result = process_pdf(file_path)
    elif file_ext in ['.jpg', '.jpeg', '.png', '.tiff', '.bmp']:
        result = process_image(file_path)
    else:
        return {
            "error": f"Unsupported file format: {file_ext}",
            "text": "",
            "success": False
        }
    
    if result.get("success"):
        # Basic resume parsing (can be enhanced)
        text = result["text"]
        result["document_type"] = "resume"
        result["contains_email"] = "@" in text
        result["contains_phone"] = any(char.isdigit() for char in text)
    
    return result


def batch_process_documents(folder_path: str, file_type: str = "pdf") -> list:
    """
    Processes multiple documents in a folder
    
    Args:
        folder_path: Path to folder containing documents
        file_type: Type of files to process ("pdf" or "image")
        
    Returns:
        List of processing results for each document
    """
    results = []
    
    if not os.path.exists(folder_path):
        return [{"error": f"Folder not found: {folder_path}"}]
    
    extensions = {
        "pdf": [".pdf"],
        "image": [".jpg", ".jpeg", ".png", ".tiff", ".bmp"]
    }
    
    valid_extensions = extensions.get(file_type, [".pdf"])
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        file_ext = os.path.splitext(filename)[1].lower()
        
        if file_ext in valid_extensions:
            if file_type == "pdf":
                result = process_pdf(file_path)
            else:
                result = process_image(file_path)
            
            results.append(result)
    
    return results


if __name__ == "__main__":
    # Test the agent
    # Note: You'll need to provide actual file paths to test
    
    # Example usage
    print("Document Processing Agent")
    print("=" * 50)
    print("Available functions:")
    print("1. process_pdf(file_path)")
    print("2. process_image(file_path)")
    print("3. process_resume(file_path)")
    print("4. batch_process_documents(folder_path, file_type)")
