import requests
import os
from langchain_pinecone import PineconeVectorStore
import pandas as pd
from langchain_text_splitters import RecursiveCharacterTextSplitter
from bs4 import BeautifulSoup
from langchain_community.document_loaders import TextLoader
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA



from langchain_openai import OpenAIEmbeddings

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
embeddings_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, model="text-embedding-ada-002")

pinecone_api_key = os.environ.get("PINECONE_API_KEY")


"""Write the full text into a text document to load later"""
def write_to_text_file(text, filename):
    with open(filename, 'w') as file:
        file.write(text)
    upload_to_pinecone(filename)


"""Uploads full piece of text to Pinecone"""
def upload_to_pinecone(output_file):
    loader = TextLoader(output_file)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings()

    index_name = "[Your Chosen Vectorstore here]"
    docsearch = PineconeVectorStore.from_documents(docs, embeddings, index_name=index_name)



url = "https://en.wikipedia.org/wiki/2023_Monaco_Grand_Prix"


"""Uses bs4 to extract information from Wikipedia"""
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    paragraphs = soup.find_all('p')
    extracted_text = [paragraph.get_text() for paragraph in paragraphs]

    full_text = '\n'.join(extracted_text)
else:
    print(f"Failed to retrieve data from the webpage. Status code: {response.status_code}")




csv_file = 'data.csv'
""""Turns the extracted information into a csv file. This is to prevent double uploads"""
filename = "output.txt"
try:
    df = pd.read_csv(csv_file)
    if full_text in df.values:
        print("Text already exists in 'data.csv'. No upload needed")
    else:
        new_df = pd.DataFrame({'String': [full_text]})

        df = pd.concat([df, new_df], ignore_index=True)

        df.to_csv(csv_file, index=False)
        print("New text is detected, changes made to csv and PineCone")
        write_to_text_file(full_text, filename)

except FileNotFoundError:
    df = pd.DataFrame({'String': [full_text]})
    df.to_csv(csv_file, index=False)
    print("New text detect and file needed. 'data.csv' file is created and text uploaded to PineCone")
    write_to_text_file(full_text, filename)



llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

embeddings = OpenAIEmbeddings()

vectorstore = PineconeVectorStore(index_name="f1-vectors", embedding=embeddings)


while True:
    query = input("Ask a question about the 2023 Monaco Grand Prix: ")
    question = (f"You are a chatbot designed to answer questions. If you do not know the answer, DO NOT make one up, simple state that you do not know the answer"
                f"Using this, and surrounding context, please answer this question:"
                f"{query}")


    vectorstore.similarity_search(query=question, k=5)

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )
    response = qa.invoke(query)["result"]

    print(response)
