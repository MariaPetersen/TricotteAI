import PyPDF2
import re
import requests
import os

class PDFProcessor:
    def __init__(self, file_id, output_file=None, vault_file=None):
        self.file_id = file_id
        self.download_url = f"https://drive.google.com/uc?export=download&id={self.file_id}"
        self.output_file = output_file or os.path.join("data", "output.pdf")
        self.vault_file = vault_file or os.path.join("data", "vault.txt")

    def download_pdf(self):
        """Downloads the PDF file from the specified URL."""
        response = requests.get(self.download_url)
        if response.status_code == 200:
            with open(self.output_file, "wb") as f:
                f.write(response.content)
            print("File downloaded successfully!")
        else:
            raise Exception(f"Failed to download the file. Status code: {response.status_code}")

    def extract_text(self):
        """Extracts text from the downloaded PDF file and splits it into chunks."""
        try:
            with open(self.output_file, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                num_pages = len(pdf_reader.pages)
                text = ''
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    if page.extract_text():
                        text += page.extract_text() + " "
                
                text = re.sub(r'\s+', ' ', text).strip()
                return text
        except FileNotFoundError:
            raise Exception("The PDF file was not found. Make sure it is downloaded.")

    def split_text_into_chunks(self, text, chunk_size=1000):
        """Splits the text into chunks of the specified size."""
        sentences = re.split(r'(?<=[.!?]) +', text)
        chunks = []
        current_chunk = ""
        for sentence in sentences:
            if len(current_chunk) + len(sentence) + 1 < chunk_size:
                current_chunk += (sentence + " ").strip()
            else:
                chunks.append(current_chunk)
                current_chunk = sentence + " "
        if current_chunk:
            chunks.append(current_chunk)
        return chunks

    def save_chunks_to_vault(self, chunks):
        """Saves the text chunks to the specified vault file."""
        with open(self.vault_file, "w", encoding="utf-8") as vault_file:
            for chunk in chunks:
                vault_file.write(chunk.strip() + "\n")
        print(f"PDF content appended to {self.vault_file} with each chunk on a separate line.")

    def process_pdf(self):
        """Main method to process the PDF: download, extract text, split into chunks, and save."""
        self.download_pdf()
        text = self.extract_text()
        chunks = self.split_text_into_chunks(text)
        self.save_chunks_to_vault(chunks)
        
    def check_existing_pdf(self):
        """Checks if the specified PDF file already exists."""
        if os.path.exists(self.output_file):
            return True
        return False

# Example usage:
if __name__ == "__main__":
    file_id = "188r6xcoIUYk9W6wJiHyfVRCGyJPFQiLu"
    processor = PDFProcessor(file_id)
    processor.process_pdf()
