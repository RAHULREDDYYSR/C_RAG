from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
#llm = ChatOpenAI(model="gpt-4o-mini")
llm = ChatGroq(model="llama-3.3-70b-versatile")
template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

generation_chain = prompt | llm | StrOutputParser()
