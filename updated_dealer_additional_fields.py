import re
import json
from groq_utils_modular import LLMHandler

class BondDataExtractor:
    def __init__(self, llm=None):
        self.llm = llm or LLMHandler()
        
    def extract_bond_data(self, message: str):
        """
        Extract bond data using simple prompt and enhanced error handling.
        """
        prompt = """Please extract bond details from the following text and provide them in a strict JSON format according to these rules:

1. Return ONLY a valid JSON object, nothing else
2. Extract the values for ISIN, security detail(info), issuer, Coupon, Maturity, Quantam(QTM), offer for each bond.
3. Include all these fields (use null if not found): 
    - isinNo (Unique 12-character alphanumeric string - e.g., 'US1234567890')
    - issuerName (string)
    - coupon (Number followed by %)
    - rating (string)
    - tenor (number)
    - quantam (Number in Lakh or Lac or L - e.g., 500000 for 5 Lakh/Lac/L, 5000000 for 50 Lakh)/Lac/L)
    - ytm (Number followed by %)
    - business_sector (Industry Name - Determine the sector this business operates in, such as "NBFC", "MFI","OTHERS", "STATE GUARANTEED","BANKING", PSU", "HFC", "INVIT", "SME". Example: "ECL FINANCE LIMITED" → "NBFC)
    - maturityDate (Format - dd/mm/yyyy)

Input text: {text}

Respond with ONLY the JSON object, no additional text or formatting."""

        messages = [
            {"role": "system", "content": prompt.format(text=message)}
        ]

        try:
            # Get response from LLM
            response = self.llm.get_response(messages)
            
            # Debug print
            # print("Raw LLM response:", response)
            
            # Clean the response
            response = response.strip()
            
            # Find the first { and last }
            start = response.find('{')
            end = response.rfind('}')
            
            if start != -1 and end != -1:
                json_str = response[start:end+1]
                # Debug print
                print("Cleaned JSON string:", json_str)
                
                try:
                    data = json.loads(json_str)
                    return [data]
                except json.JSONDecodeError as e:
                    print(f"JSON parsing error: {e}")
                    return self.fallback_extraction(message)
            else:
                print("No valid JSON found in response")
                return self.fallback_extraction(message)
                
        except Exception as e:
            print(f"Error in LLM extraction: {e}")
            return self.fallback_extraction(message)

    def fallback_extraction(self, message: str):
        """
        Fallback regex-based extraction method.
        """
        # Initialize empty bond data
        bond_data = {
            "isinNo": None,
            "issuerName": None,
            "coupon": None,
            "rating": None,
            "tenor": None,
            "quantam": None,
            "ytm": None,
            "business_sector": None,
            "maturityDate": None
        }

        # Extract ISIN
        isin_match = re.search(r"ISIN\s*:?\s*([A-Z]{2}[A-Z0-9]{9}\d)", message)
        if isin_match:
            bond_data["isinNo"] = isin_match.group(1)

        # Extract issuer name (assumes it's the first capitalized word)
        issuer_match = re.search(r"([A-Z]+(?:\s[A-Z]+)*)", message)
        if issuer_match:
            bond_data["issuerName"] = issuer_match.group(1)

        # Extract coupon rate
        coupon_match = re.search(r"(\d{1,2}\.\d{1,2})\s*(?:NCD|%)", message)
        if coupon_match:
            bond_data["coupon"] = float(coupon_match.group(1))

        # Extract quantam
        quantam_match = re.search(r"(\d+)\s*L", message)
        if quantam_match:
            bond_data["quantam"] = int(quantam_match.group(1))

        # # Extract bid/offer
        # bid_match = re.search(r"Bidding at (\d{1,2}\.\d{1,2})%", message)
        # if bid_match:
        #     bond_data["bid_offer"] = float(bid_match.group(1))

        # Extract maturity date
        maturity_match = re.search(r"(\d{2}[A-Z]{2}\d{2})", message)
        if maturity_match:
            date_str = maturity_match.group(1)
            # Convert date like "12JU26" to "2026-06-12"
            month_map = {
                'JA': '01', 'FE': '02', 'MR': '03', 'AP': '04',
                'MY': '05', 'JU': '06', 'JL': '07', 'AU': '08',
                'SE': '09', 'OC': '10', 'NO': '11', 'DE': '12'
            }
            try:
                day = date_str[:2]
                month = month_map.get(date_str[2:4], '01')
                year = '20' + date_str[4:]
                bond_data["maturityDate"] = f"{year}-{month}-{day}"
            except:
                pass

        return [bond_data]

def main():
    extractor = BondDataExtractor()
    
    while True:
        print("\nChoose input method:")
        print("1: File input")
        print("2: Manual input")
        print("3: Exit")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == '3':
            break
            
        if choice == '1':
            filename = input("Enter filename: ").strip()
            try:
                with open(filename, 'r') as f:
                    text = f.read().strip()
            except FileNotFoundError:
                print(f"File {filename} not found!")
                continue
        elif choice == '2':
            print("Enter bond details :")
            text = input().strip()
            # lines = []
            # while True:
            #     line = input()
            #     if not line:
            #         break
            #     lines.append(line)
            # text = "\n".join(lines)
        else:
            print("Invalid choice!")
            continue

        try:
            results = extractor.extract_bond_data(text)
            print("\nExtracted Data:")
            print(json.dumps(results, indent=2))
        except Exception as e:
            print(f"Error: {str(e)}")
            print("Falling back to regex extraction...")
            results = extractor.fallback_extraction(text)
            print("\nExtracted Data (using fallback):")
            print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
