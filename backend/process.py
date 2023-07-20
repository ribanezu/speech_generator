import re
import chromadb
from chromadb.config import Settings
from PyPDF2 import PdfReader

document_id = 1


def process_files(documents):
    chroma_client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet",
                                             persist_directory="local_db"
                                             ))
    
    #if chroma_client.get_collection(name="tender_doc"):
    #    chroma_client.delete_collection(name="tender_doc")
    collection = chroma_client.get_or_create_collection(name="tender_doc")
    #for file in documents:
    #    print("processing file: " + file.filename)
    #    markdown_text = file.read().decode()
    #    chunks = split_text(markdown_text)
    #    document_title = get_title(markdown_text)
    #    generate_embeddings(chunks, document_title, file.filename, collection)
    #chroma_client.persist()

    for file in documents:
        print("processing file: " + file.filename)
        chunks = get_text_from_pdf_chunks(file)
        #chunks = split_text(text)
        print("número de chunks "+str(len(chunks)))
        document_title = str(file.filename)
        #document_title = get_title(file.filename)
        generate_embeddings(chunks, document_title, file.filename, collection)
    chroma_client.persist()


def get_text_from_pdf_chunks(file_path):
    pdf_reader = PdfReader(file_path)
    num_pages = len(pdf_reader.pages)
    chunks = []
    print("number of pages: " + str(len(pdf_reader.pages)))
    for page in range(num_pages):
        page_obj = pdf_reader.pages[page]
        print("len of page: " + str(len(page_obj.extract_text())))
        chunks.append(page_obj.extract_text())
    return chunks


def process_files_knowledge(documents):
    chroma_client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet",
                                             persist_directory="local_db"
                                             ))
    chroma_client.delete_collection(name="pastbid")
    collection = chroma_client.get_or_create_collection(name="pastbid")
    #for file in documents:
    #    print("processing file: " + file.filename)
    #    markdown_text = file.read().decode()
    #    chunks = split_text(markdown_text)
    #    document_title = get_title(markdown_text)
    #    generate_embeddings(chunks, document_title, file.filename, collection)
    #chroma_client.persist()

    for file in documents:
        print("processing file: " + file.filename)
        chunks = get_text_from_pdf_chunks(file)
        #chunks = split_text(text)
        print("número de chunks "+str(len(chunks)))
        document_title = str(file.filename)
        #document_title = get_title(file.filename)
        generate_embeddings(chunks, document_title, file.filename, collection)
    chroma_client.persist()


def get_text_from_pdf_chunks(file_path):
    pdf_reader = PdfReader(file_path)
    num_pages = len(pdf_reader.pages)
    chunks = []
    print("number of pages: " + str(len(pdf_reader.pages)))
    for page in range(num_pages):
        page_obj = pdf_reader.pages[page]
        print("len of page: " + str(len(page_obj.extract_text())))
        chunks.append(page_obj.extract_text())
    return chunks



def get_text_from_pdf(file_path):
    pdf_reader = PdfReader(file_path)
    num_pages = len(pdf_reader.pages)
    full_text = ""
    for page in range(num_pages):
        page_obj = pdf_reader.pages[page]
        full_text += page_obj.extract_text()
    return full_text

def generate_embeddings(chunks, document_title, file_name, collection):
    global document_id
    j=1
    for chunk in chunks:
        # Generamos el id del documento
        doc_id = str(document_id)
        # Intentamos recuperar un documento con este ID
        existing_document = collection.get(ids=[doc_id])
        # Si el documento no existe, lo agregamos a la colección
        if existing_document:
            collection.delete(ids=[doc_id])
        collection.add(
            metadatas={
                "document_title": document_title if document_title is not None else "",
                "file_name": file_name,
                "page": str(j)
            },
            documents=chunk,
            ids=[str(document_id)]
        )
        document_id = document_id + 1
        j=j+1


def get_title(file):
    match = re.search(r"title:\s+(.+)\s+", file)
    if match:
        title = match.group(1)
        return title
    else:
        " "

# Pendiente implementar lógica de separación en chunks.
def split_text(file):
    sections = re.split('\d+\.\d+\.\d+\ ', file)
    for i, section in enumerate(sections):
        print(f"Section {i+1} has {len(section)} characters.")
    return sections
    #separator = "\n### "
    #return file.split(separator)


def query_collection(query):
    chroma_client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet",
                                             persist_directory="local_db"
                                             ))
    collection = chroma_client.get_or_create_collection(name="tender_doc")
    return collection.query(
        query_texts=[query],
        n_results=3,
    )

def query_collection_knowledge(query):
    chroma_client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet",
                                             persist_directory="local_db"
                                             ))
    collection = chroma_client.get_or_create_collection(name="pastbid")
    return collection.query(
        query_texts=[query],
        n_results=3,
    )