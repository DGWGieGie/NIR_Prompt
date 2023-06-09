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
        
    
    def run(self, API):
        openai.api_key = API
        count = 0
        total = 0
        for i in self.validL[:]:#[:10] + cand_ids[49:57] + cand_ids[75:81]:
            
            candidate_items =  self.candiSet.getCandidate(i, self.similaritys.getSimilaritys(i), self.considerSize, self.num_cand, self.target)
            random.shuffle(candidate_items)

            input_1 = utils.temp_1.format(', '.join(candidate_items), ', '.join(self.candiSet.uiData[i][0].split(" | ")[-self.length_limit:]))

            try:
                response = openai.Completion.create(
                        engine="text-davinci-003",
                        prompt=input_1,
                        max_tokens=512,
                        temperature=0,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0,
                        n = 1,
                    )
            except Exception as e:
                if 'exceeded your current quota' in str(e):
                    print("Input1: exceeded your current quota")

            predictions_1 = response["choices"][0]['text']
    
    
            input_2 = utils.temp_2.format(', '.join(candidate_items), ', '.join(self.candiSet.uiData[i][0].split(" | ")[-self.length_limit:]), predictions_1)

            time.sleep(2)
            try:
                response = openai.Completion.create(
                        engine="text-davinci-003",
                        prompt=input_2,
                        max_tokens=512,
                        temperature=0,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0,
                        n = 1,
                    )

            except Exception as e:
                if 'exceeded your current quota' in str(e):
                    print("Input2: exceeded your current quota")

            predictions_2 = response["choices"][0]['text']
    
    
            input_3 = utils.temp_3.format(', '.join(candidate_items), ', '.join(self.candiSet.uiData[i][0].split(" | ")[-self.length_limit:]), predictions_1, predictions_2)

            time.sleep(2)
            try:
                response = openai.Completion.create(
                        engine="text-davinci-003",
                        prompt=input_3,
                        max_tokens=512,
                        temperature=0,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0,
                        n = 1,
                    )
                try_nums = 0
                kk_flag = 1
            except Exception as e:
                if 'exceeded your current quota' in str(e):
                    print("Input3: exceeded your current quota")

            predictions = response["choices"][0]['text']
    

            hit_=0
            if self.candiSet.uiData[i][-1] in predictions:
                count += 1
                hit_ = 1
            else:
                pass
            total +=1
    
            print (f"GT:{self.candiSet.uiData[i][-1]}")
            print (f"predictions:{predictions}")
    
            print (f'PID:{i}; count/total:{count}/{total}={count*1.0/total}\n')
            result_json = {"PID": i,
                        "Input_1": input_1,
                        "Input_2": input_2,
                        "Input_3": input_3,
                        "GT": self.candiSet.uiData[i][-1],
                        "Predictions_1": predictions_1,
                        "Predictions_2": predictions_2,
                        "Predictions": predictions,
                        'Hit': hit_,
                        'Count': count,
                        'Current_total':total,
                        'Hit@10':count*1.0/total}
            self.results_data.append(result_json)

    def save(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.results_data, f, ensure_ascii=False, indent=2)
        
