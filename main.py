
from ai.ollama_functions import Ollama
from ai.upload import PDFProcessor
from console.settings import AISettings
import argparse
from constants.colors import CYAN, YELLOW, PINK, NEON_GREEN, RESET_COLOR

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ollama Chat")
    parser.add_argument("--model", default="llama3.2", help="Ollama model to use (default: llama3.2)")
    args = parser.parse_args()
    temperature = 0.3
    
    def set_temperature(value):
        global temperature
        temperature = value
        print(PINK + f"Temperature set to: {temperature}" + RESET_COLOR)

    ollama_class = Ollama(args.model)
    ai_settings = AISettings()
    
    while True:
        ai_settings.ask_temperature()
        ai_settings.ask_document_settings()
        user_input = input(YELLOW + "Ask something about knitting (or type 'quit' to exit): " + RESET_COLOR)
        print(CYAN + "Let me think about all this..." + RESET_COLOR)
        if user_input.lower() == 'quit':
            break
        if ai_settings.file_id:
            processor = PDFProcessor(ai_settings.file_id)
            if not processor.check_existing_pdf():
                processor.process_pdf()
            response = ollama_class.ollama_chat(user_input, temperature)
        else:
            print(CYAN + "Answering your question without using a RAG" + RESET_COLOR)
            response = ollama_class.ollama_no_rag_chat(user_input, temperature)
            
        print(NEON_GREEN + "Response: \n\n" + response + RESET_COLOR)
