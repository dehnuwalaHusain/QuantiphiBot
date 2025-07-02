from langchain.memory import ConversationBufferMemory

MEMORY_STORE = {}

def get_memory_for_user ( user_id ) -> ConversationBufferMemory:
    if user_id not in MEMORY_STORE:
        MEMORY_STORE[user_id] = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )
    return MEMORY_STORE[user_id]
