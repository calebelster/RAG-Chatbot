# RAG Chatbot
Utilized a Pinecone vector database, LangChain, and Hugging Face to create a RAG (Retrieval-Augmented Generation) chatbot capable of utilizing a large .txt file of fun facts to answer specific questions from the user about any topic covered in the file.
### Run:
1. Create a Pinecone account and create a new project.
2. Create a Hugging Face account and generate a new access tokens with the correct permissions.
3. Create a new .env file and add the API keys from Pinecone and Hugging Face under the names HUGGINGFACE_API_KEY and PINECONE_API_KEY. 
4. Run the following command in the terminal while in the project directory to install the necessary libraries:
```
pip install -r requirements.txt
```
5. Run the following command in the terminal while in the project directory to run the script:
```
streamlit run frontend-streamlit.py
```
#### References:
- funfacts.txt file from: https://github.com/anfederico/fact-bot/tree/master
- Tutorial for chatbot from: https://medium.com/credera-engineering/build-a-simple-rag-chatbot-with-langchain-b96b233e1b2a