from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
from langchain_community.vectorstores import Pinecone
import pinecone
import os
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain.prompts import PromptTemplate
from langchain_community.llms import HuggingFaceEndpoint

class ChatBot():

    load_dotenv()
    loader = TextLoader("funfacts.txt", encoding="utf-8")
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=4)
    docs = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings()



    # Initialize Pinecone client
    pinecone.init(
        api_key=os.getenv('PINECONE_API_KEY'),
        environment='gcp-starter'
    )

    # Define Index Name
    index_name = "langchain-demo"

    # Checking Index
    if index_name not in pinecone.list_indexes():
        # Create new Index
        pinecone.create_index(name=index_name, metric="cosine", dimension=768)
        docsearch = Pinecone.from_documents(docs, embeddings, index_name=index_name)
    else:
        # Link to the existing index
        docsearch = Pinecone.from_existing_index(index_name, embeddings)

    repo_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
    llm = HuggingFaceEndpoint(
        repo_id=repo_id,
        temperature=0.8,
        top_k=50,
        huggingfacehub_api_token=os.getenv('HUGGINGFACE_API_KEY')
    )


    template = """
    You are a knowledgeable source of fun facts for whoever is curious. The Human will ask you about different fun facts for entertainment. 
    Use following piece of context to answer the question. 
    If you don't know the answer, just say you don't know. 
    Keep the answer within 2 sentences and concise.

    Context: {context}
    Question: {question}
    Answer: 

    """

    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )

    rag_chain = (
            {"context": docsearch.as_retriever(), "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
    )