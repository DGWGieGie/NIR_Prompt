import json

def read_json(file):
    with open(file) as f:
        return json.load(f)

temp_1 = """
Candidate Set (candidate movies): {}.
The movies I have watched (watched movies): {}.
Step 1: What features are most important to me when selecting movies (Summarize my preferences briefly)? 
Answer: 
"""

temp_2 = """
Candidate Set (candidate movies): {}.
The movies I have watched (watched movies): {}.
Step 1: What features are most important to me when selecting movies (Summarize my preferences briefly)? 
Answer: {}.
Step 2: Selecting the most featured movies from the watched movies according to my preferences (Format: [no. a watched movie.]). 
Answer: 
"""

temp_3 = """
Candidate Set (candidate movies): {}.
The movies I have watched (watched movies): {}.
Step 1: What features are most important to me when selecting movies (Summarize my preferences briefly)? 
Answer: {}.
Step 2: Selecting the most featured movies (at most 5 movies) from the watched movies according to my preferences in descending order (Format: [no. a watched movie.]). 
Answer: {}.
Step 3: Can you recommend 10 movies from the Candidate Set similar to the selected movies I've watched (Format: [no. a watched movie - a candidate movie])?.
Answer: 
"""

candidatePrompt = """
It is random Candidate Set with random sequence (candidate movies): {}.
"""

prompt1 = """
The movies I have watched (watched movies): {}.
What features are most important to me when selecting movies (Summarize my preferences briefly)? 
"""

prompt2 = """
Selecting the 8 most featured movies from the watched movies according to my preferences (Format: [no. a watched movie.]). 
"""

prompt3 = """
Can you recommend 10 movies from the Candidate Set similar to the selected movies I've watched (Format: [no. a watched movie - a candidate movie])?.
"""

exchange_prompt1 = """
The movies I have watched (watched movies): {}.
Selecting the 8 most featured movies from the watched movies (Format: [no. a watched movie.]). 
"""

exchange_prompt2 = """
What features are most important to me when selecting movies (Summarize my preferences briefly)? 
"""

exchange_prompt3 = """
After summarizing my preferences, selecting the 8 most featured movies from the watched movies again (Format: [no. a watched movie.]). 
"""

promptLearn1 = """
The movies I have watched (watched movies): {}.
Can you recommend 10 movies from the Candidate Set similar to the selected movies I've watched (Format: [no. a watched movie - a candidate movie])?.
"""

promptLearn2 = """
What features are most important to me when selecting movies according to watched movies (Summarize my preferences briefly)? 
"""

promptLearn3 = """
After summarizing my preferences, could you modify/refine the recommended movies list? (Format: [no. a watched movie.]). 
"""
