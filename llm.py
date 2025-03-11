import json
import ollama

# System prompt for the LLM
SYS_PROMPT = (
    "You are a network graph maker who extracts terms and their relations from a given context. "
    "You are provided with a context chunk (delimited by ```) Your task is to extract the ontology "
    "of terms mentioned in the given context. These terms should represent the key concepts as per the context. \n"
    "Thought 1: While traversing through each sentence, think about the key terms mentioned in it.\n"
    "\tTerms may include object, entity, location, organization, person, \n"
    "\tcondition, acronym, documents, service, concept, etc.\n"
    "\tTerms should be as atomistic as possible\n\n"
    "Thought 2: Think about how these terms can have one-on-one relations with other terms.\n"
    "\tTerms that are mentioned in the same sentence or the same paragraph are typically related to each other.\n"
    "\tTerms can be related to many other terms\n\n"
    "Thought 3: Find out the relation between each such related pair of terms. \n\n"
    "Format your output as a list of JSON. Your only response should always be the JSON output without showing any "
    "thought process or functioning. Each element of the list contains a pair of terms and the relation between them, "
    "like the following:\n"
    "[\n"
    "  {\n"
    "    \"node_1\": \"A concept from extracted ontology\",\n"
    "    \"node_2\": \"A related concept from extracted ontology\",\n"
    "    \"edge\": \"relationship between the two concepts, node_1 and node_2 in one or two sentences\"\n"
    "  },\n"
    "  {...}\n"
    "]"
)

# User prompt template
USER_PROMPT = "context: ```{}``` \n\n output: "

def generate_json_and_save_to_file(text, filename='output.json'):
    """
    Generate JSON output from LLM and save it to a file.

    Parameters:
    - text (str): The input context text for the LLM.
    - filename (str): The filename to save the JSON output. Default is 'output.json'.
    """

    prompt = USER_PROMPT.format(text)
    
    try:
        response = ollama.chat(model="kg_good", messages=[ {"role": "user", "content": prompt}])
        
        print("Response from LLM:", response)
        
        content = response['message']['content']  # Correct way to access content
        
        if not content:
            raise ValueError("Empty response content from LLM.")
        
        data = json.loads(content)  # Convert string response into a list of dictionaries
        
        with open('output.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)  # Save JSON to file
        print(f"LLM output saved successfully to output.json.")
    
    except KeyError:
        print("Error: Invalid response format from the LLM.")
    except json.JSONDecodeError:
        print("Error decoding JSON from the LLM response.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

text = '''John walked into the coffee shop and greeted Sarah, the barista. They talked about their favorite books while she prepared his espresso. As John left, he promised to return the next day for another chat.'''

generate_json_and_save_to_file(text)
