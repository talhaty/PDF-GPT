import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts.prompt import PromptTemplate
from langchain_community.callbacks import get_openai_callback
from langchain.memory import ConversationBufferWindowMemory



if 'initialized' not in st.session_state:
    st.session_state.initialized = True


class Chatbot:

    def __init__(self, model_name, temperature, vectors):
        self.model_name = model_name
        self.temperature = temperature
        self.vectors = vectors
        self.memory = ConversationBufferWindowMemory(memory_key="chat_history", k=10, return_messages=True)

    qa_template = """
        You are a helpful AI assistant named Alt bot. The user gives you a file its content is represented by the following pieces of context, use them to answer the question at the end.
        If you don't know the answer, just say you don't know. Do NOT try to make up an answer.
        If the question is not related to the context, politely respond that you are tuned to only answer questions that are related to the context.
        Use as much detail as possible when responding.

        context: {context}
        =========
        question: {question}
        ======
        """

    QA_PROMPT = PromptTemplate(template=qa_template, input_variables=["context","question" ])

    def conversational_chat(self, query):
        """
        Start a conversational chat with a model via Langchain
        """
        llm = ChatOpenAI(model_name=self.model_name, temperature=self.temperature)

        retriever = self.vectors.as_retriever()


        chain = ConversationalRetrievalChain.from_llm(llm=llm,
            retriever=retriever, verbose=True, return_source_documents=True, max_tokens_limit=1024, combine_docs_chain_kwargs={'prompt': self.QA_PROMPT})

        chain_input = {"question": query, "chat_history": st.session_state["history"]}
        
        with get_openai_callback() as cb:
            result = chain(chain_input)
            st.write(f'###### Total cost : {cb.total_cost} $')
            st.write(f'###### Total tokens : {cb.total_tokens}')
            st.write(f'###### Prompt Tokens : {cb.prompt_tokens}')
            st.write(f'###### Completion Tokens : {cb.completion_tokens}')
        

        st.session_state["history"].append((query, result["answer"]))
        #count_tokens_chain(chain, chain_input)
        return result["answer"]
    
    




    
    
