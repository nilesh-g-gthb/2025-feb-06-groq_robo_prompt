from groq_utils_modular import LLMHandler

# - questions related to information about a Fixed Income security
# - question related to price negotiation
# - questions related to settlement of transactions
# - information about a transaction done or to be done
# - questions related to planning for transaction execution

# Improved Prompts on 10th Feb
CLASSIFICATION_INSTRUCTIONS = """ Instruction: You are a supervisor managing chat messages related to Fixed Income instruments. Your task is to classify each message based on intent and not based on some word in the message, ensuring accurate routing.

There are three possible categories:

      BidRequest – The user is looking to buy or is asking for a bid price.
        Examples:
            "Any offers for XYZ bond?"
            "Looking to buy XYZ, any sellers?"
            "What’s your offer on XYZ?"
	        "Need offers XYZ, what’s available?"
	        "What’s the lowest ask?"
	        "let me know what’s on offer."
	        "Anyone selling XYZ bonds? Looking at 5.5% yield."

    OfferRequest – The user is looking to sell or is asking for an offer price.
        Examples:
            "Selling XYZ bond, any bid?"
            "Any takers for XYZ at 5.2% yield?"
	        "available at 4.8% yield, any takers?"
	        "Looking to sell AAA-rated bonds, send your bids."
	        "treasury bonds, who wants in?"
            "Offloading XYZ, who’s interested?
            

    General – If the intent is unclear, classify as "general" instead of making assumptions. 
    
    Respond with only one word: "BidRequest", "OfferRequest", or "General"
    
    """

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
