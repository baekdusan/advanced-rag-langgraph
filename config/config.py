import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

# API 키 설정
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# 모델 설정
MODEL_NAME = "gpt-4o-mini"
TEMPERATURE = 0

# LLM 초기화
llm = ChatOpenAI(model=MODEL_NAME, temperature=TEMPERATURE)

# 벡터 저장소 설정
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
COLLECTION_NAME = "rag_pdf_db" 