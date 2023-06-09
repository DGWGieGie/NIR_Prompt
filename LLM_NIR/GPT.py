import time
import json
import utils
import openai
import random 
import candidateSet

class Prompt:
    def __init__(self, candiSet:candidateSet.uiMatrix, similaritys:candidateSet.Similarity,
                 validL, length_limit, considerSize, num_cand, target, random_seed) -> None:
        
        self.length_limit = length_limit
        self.candiSet = candiSet
        self.similaritys = similaritys
        self.validL = validL
        self.considerSize = considerSize
        self.num_cand = num_cand
        self.target = target
        self.random_seed = random.seed(random_seed)
        self.results_data = []
        print("Using GPT")
        
    def prompting(self, message):
        try_num = 1
        while try_num:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages = message,
                    max_tokens=512,
                    temperature=0,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0,
                    n = 1,
                    )
                try_num = 0
            except Exception as e:
                print("Prompting Wrong: ",e)
                time.sleep(2)
        return response['choices'][0]['message']['content']
    
    def envReflection(self, message, predictions_3, target):

        message.append({"role": "assistant", "content": predictions_3})
        message.append({"role": "user", "content": utils.envRefPrompt1})
        envPredictions_1 = self.prompting(message)
    
        message.append({"role": "assistant", "content": envPredictions_1})
        message.append({"role": "user", "content": utils.envRefPrompt2})
        envPredictions_2 = self.prompting(message)
        
        return envPredictions_2
    
    def fewShotEng(self, message):
        message.append({"role": "user", "content": ""})
        for _ in range(10):
            while True:
                try:
                    response = openai.Completion.create(
                        # model="ada:ft-easyshare-2023-06-07-12-44-37",
                        model="ada:ft-easyshare-2023-06-08-03-00-33",
                        prompt=message[-3]["content"]+message[-2]["content"],
                        max_tokens=2,
                        temperature=0,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0,
                        n = 1)
                    break
                except Exception as e:
                    print("Prompting Wrong: ",e)
                    time.sleep(2)
            out = response['choices'][0]['text'].strip(" .\n")
            if out == "inconcrete":
                message[-1]["content"] = "It is inconcrete, please consider more concrete."
                message[-2]["content"] = self.prompting(message)
            elif out == "imperfect":
                message[-1]["content"] = "It is imperfect, please consider deeper."
                message[-2]["content"] = self.prompting(message)
            elif out == "wrong":
                message[-1]["content"] = "It is imperfect, could you please consider deeper with summarizing it briefly."
                message[-2]["content"] = self.prompting(message)
            else:
                break
        return message[:-1]
        
        
    def run(self, API):
        openai.api_key = API
        count = 0
        total = 0
        for i in self.validL[:]:#[:10] + cand_ids[49:57] + cand_ids[75:81]:
            
            candidate_items =  self.candiSet.getCandidate(i, self.similaritys.getSimilaritys(i), self.considerSize, self.num_cand, self.target)
            random.shuffle(candidate_items)
            
            candidatePrompt = utils.candidatePrompt.format(', '.join(candidate_items))

            prompt_1 = utils.prompt1.format(', '.join(self.candiSet.uiData[i][0].split(" | ")[-self.length_limit:]))
            
            message = [{"role": "system", "content": candidatePrompt}, 
                       {"role": "user", "content": prompt_1}]

            predictions_1 = self.prompting(message)
            message.append({"role": "assistant", "content": predictions_1})
            # message = self.fewShotEng(message)
            # predictions_1 = message[-1]["content"]
        
            message.append({"role": "user", "content": utils.prompt2})

            predictions_2 = self.prompting(message)
            
            message.append({"role": "assistant", "content": predictions_2})
            message.append({"role": "user", "content": utils.prompt3})

            predictions = self.prompting(message)
            
            hit_=0
            if self.candiSet.uiData[i][-1] in predictions:
                count += 1
                hit_ = 1
            else:
                pass
            total +=1
    
            print (f"GT:{self.candiSet.uiData[i][-1]}")
            print (f"Refine Summary:{predictions_1}")
            print (f"predictions:{predictions}")
    
            print (f'PID:{i}; count/total:{count}/{total}={count*1.0/total}\n')

            result_json = {"PID": i,
                        "CandidateSet":candidatePrompt,
                        "GT": self.candiSet.uiData[i][-1],
                        "content":message,
                        "Predictions": predictions,
                        'Hit': hit_,
                        'Count': count,
                        'Current_total':total,
                        'Hit@10':count*1.0/total}
            
            self.results_data.append(result_json)  

    def save(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.results_data, f, ensure_ascii=False, indent=2)
