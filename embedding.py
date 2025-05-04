from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY') # ~/.zshrc 에서 key 값 받아오기

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
openai_embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("A Study on the Implementation Method of an Agent-Based Advanced RAG System Using Graph.pdf") # RAG 논문 파일 경로
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50) # 500자씩 잘라서 중복 50자씩 넣기
chunked_docs = text_splitter.split_documents(documents)
chunked_docs[:2]

# Load the documents to vectorstore
# 자른 문서를 벡터 저장소에 로드. 임베딩 모델 사용
vectorstore = Chroma.from_documents(
    documents=chunked_docs,
    collection_name="rag_pdf_db",
    embedding=openai_embeddings
)
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 10}, # 검색 결과 10개 반환
    threshold=0.7 # 검색 결과 최소 0.7 이상 반환
) # 벡터 저장소에서 검색 가능한 객체 생성, 검색 쿼리 전달 시 검색 결과 반환

results = retriever.invoke("What is Adaptive RAG?")

