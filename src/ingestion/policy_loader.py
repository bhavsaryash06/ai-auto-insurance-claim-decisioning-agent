from pathlib import Path
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def extract_policy_text(policy_file_path: str) -> str:
    """
    Extract raw text from a policy PDF using pypdf.
    """
    reader = PdfReader(policy_file_path)

    extracted_text = ""

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text()

        if page_text:
            extracted_text += f"\n\n--- PAGE {page_number} ---\n\n"
            extracted_text += page_text

    return extracted_text.strip()


def load_policy_documents(policy_folder_path: str = "data/policies") -> list[dict]:
    """
    Load all policy PDFs from the policy folder.
    Returns a list of dictionaries with filename and extracted text.
    """
    policy_folder = Path(policy_folder_path)

    pdf_files = sorted(policy_folder.glob("*.pdf"))

    documents = []

    for pdf_file in pdf_files:
        text = extract_policy_text(str(pdf_file))

        documents.append(
            {
                "source": pdf_file.name,
                "file_path": str(pdf_file),
                "text": text,
            }
        )

    return documents


def chunk_policy_documents(
    policy_folder_path: str = "data/policies",
    chunk_size: int = 1000,
    chunk_overlap: int = 150,
) -> list[dict]:
    """
    Load policy PDFs and split them into smaller text chunks.
    Each chunk keeps source metadata.
    """
    documents = load_policy_documents(policy_folder_path)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    chunks = []

    for doc in documents:
        split_texts = text_splitter.split_text(doc["text"])

        for index, chunk_text in enumerate(split_texts):
            chunks.append(
                {
                    "source": doc["source"],
                    "file_path": doc["file_path"],
                    "chunk_id": f"{doc['source']}_chunk_{index + 1}",
                    "text": chunk_text,
                }
            )

    return chunks