from tavily import TavilyClient
from dotenv import load_dotenv
import os 

load_dotenv()

API_KEY = os.getenv("TAVILY_API_KEY")
tavily_client = TavilyClient(api_key=API_KEY)

def tavily_search(query):
    try:
        response = tavily_client.search(query=query, max_results=5)        
        results = []
        
        if "results" in response:
            for i, r in enumerate(response["results"], 1):
                title = r.get("title", "Unknown")
                url = r.get("url", "Unknown")
                snippet = r.get("content", "Unknown")

                # Properly truncate the snippet inside the loop
                if len(snippet) > 300:
                    snippet = snippet[:300].rsplit(" ", 1)[0] + "..."
                
                # Append the formatted dictionary to your list
                results.append(f"{i} **{title}**\n {url}\n {snippet}" )
            
            return "\n\n".join(results)  # Return the collected results
            
        else:
            print("No results found in the response.")
            return []
            
    except Exception as e:
        print(f"An error occurred during the search: {e}")
        return None

# Test the function
if __name__ == "__main__":
    search_results = tavily_search("Is charges will occur on UPI payment for merchant account in India")
    print(search_results)