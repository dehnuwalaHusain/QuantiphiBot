import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain_groq import ChatGroq
from langchain.docstore.document import Document

from memory_store import get_memory_for_user
from user_access import USER_ACCESS

INDEX_ROOT = "vector_store"
embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

llm = ChatGroq(
    groq_api_key=os.environ["GROQ_API_KEY"],
    model_name="Llama-3.3-70b-Versatile"
)

def get_chain ( user_email ):
    companies = USER_ACCESS.get ( user_email, [])
    all_dbs = []

    for company in companies:
        index_path = os.path.join ( INDEX_ROOT, company )
        if os.path.exists ( index_path ):
            db = FAISS.load_local ( index_path, embedder, allow_dangerous_deserialization=True )
            all_dbs.append(db)
        else:
            print("Index missing for ", company)

    if (all_dbs == []):
        raise ValueError("No accessible indexes for this user")

    main_db = all_dbs[0]
    for db in all_dbs[1:]:
        main_db.merge_from(db)

    memory = get_memory_for_user ( user_email )

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=main_db.as_retriever(search_kwargs={"k": 5}),
        memory=memory,
        return_source_documents=False
    )
    return chain