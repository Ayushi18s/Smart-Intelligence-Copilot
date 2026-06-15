chat_memory = []

def add_memory(question, answer):
    chat_memory.append({"q": question, "a": answer})

def get_memory():
    return chat_memory[-5:]  # last 5 interactions