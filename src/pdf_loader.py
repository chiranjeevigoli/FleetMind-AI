#Import the PyMuPDF library to read PDF files
import fitz

#Imort os to work with file and folder paths
import os

def load_documents(folder_path):
    """
    Reads all PDF files from the given folder and extracts
    text page by page.

    Args:
        folder_path (str): Path to the folder containing PDF manuals.

    Returns:
        list: A list of dictionaries containing
              source filename, page number, and page text.
    """

    #Empty list to store all extracted pages

    documents = []

    #Iterate through every file inside the manuals folder

    for filename in os.listdir(folder_path):

        #Process only PDF files
        if filename.endswith(".pdf"):

            #create the complete path of the PDF
            pdf_path = os.path.join(folder_path, filename)

            #Open the PDF document
            pdf = fitz.open(pdf_path)

            #Loop through every page in the PDF

            for page_num in range(len(pdf)):

                #Loop one page at a time
                page = pdf.load_page(page_num)

                #Extract text from the current page
                text = page.get_text()

                #Store userful information for future retrieval

                documents.append({
                    "source":filename,
                    "page":page_num + 1,
                    "text":text
                })
    return documents

# Execute only when this file is run directly

if __name__ == "__main__":
     # Read all manuals from the folder
    docs = load_documents("data/manuals")

    # Display the total number of pages extracted
    print(f"Total Pages Loaded: {len(docs)}")

    print("\nFirst Page Preview:\n")

    # Display the first 1000 characters of the first page
    print(docs[0]["text"][:1000])

    