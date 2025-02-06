from groq_utils_modular import LLMHandler

# - questions related to information about a Fixed Income security
# - question related to price negotiation
# - questions related to settlement of transactions
# - information about a transaction done or to be done
# - questions related to planning for transaction execution

CLASSIFICATION_INSTRUCTIONS = """Instruction: You are a supervisor tasked with managing the chat messages with queries about Fixed Income instruments, an AI assistant. Your task is to classify the incoming questions. Depending on your answer, which needs to be a single word, question will be routed to the right team, so your task is crucial for our team. There are two possible question types:
1. QuoteRequest 
- questions related to price, bid, offer for a given Fixed Income security

2. General
- general questions"""

def classify_query(llm, user_input):
    messages = [
        {"role": "system", "content": CLASSIFICATION_INSTRUCTIONS},
        {"role": "user", "content": user_input}
    ]
    return llm.get_response(messages)

def main():
    llm = LLMHandler()
    while True:
        try:
            user_input = input("\nEnter your query (or 'exit'): ").strip()
            
            if user_input.lower() == 'exit':
                break
            
            if not user_input:
                continue
            
            classification = classify_query(llm, user_input)
            print(f"\nClassification: {classification}")
            
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
