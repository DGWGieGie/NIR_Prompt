import argparse

# import LLM
import GPT
import candidateSet


parser = argparse.ArgumentParser()

parser.add_argument('--filename', type=str, default="ml-100k_NIR1.json", help='')
parser.add_argument('--USER', type=int, default=1, help='')
parser.add_argument('--RATING', type=int, default=0, help='')
parser.add_argument('--similarity', type=str, default="baseline", help='baseline|cosine|euclidean|jaccard|manhattan')
parser.add_argument('--length_limit', type=int, default=8, help='')
parser.add_argument('--considerSize', type=int, default=13, help='')
parser.add_argument('--num_cand', type=int, default=19, help='')
parser.add_argument('--target', type=int, default=0, help='')
parser.add_argument('--random_seed', type=int, default=42, help='')
parser.add_argument('--API', type=str, default="sk-", help="")
parser.add_argument('--saveFile', type=str, default="baseline.json", help="")

args = parser.parse_args()

cS = candidateSet.uiMatrix(args.filename, USER=args.USER, RATING=args.RATING)

similaritys = candidateSet.Similarity(cS.uiMatrix, args.similarity.split('|'))

count = 0
total = 0
validList = []
if args.USER:
    for i in range(len(cS.uiData)):
        target = cS.uiData[i]
        
        candidate_items = cS.getCandidate(i, similaritys.getSimilaritys(i), args.considerSize, args.num_cand, args.target)

        if target[-1] in candidate_items:
            count += 1
            validList.append(i)
        total +=1
    print (f'count/total:{count}/{total}={count*1.0/total}')
    print ('-----------------\n')
    
    # prompt = LLM.Prompt(cS, similaritys, validList, args.length_limit, args.considerSize, 
    #            args.num_cand, args.target, args.random_seed)
    
    prompt = GPT.Prompt(cS, similaritys, validList, args.length_limit, args.considerSize, 
               args.num_cand, args.target, args.random_seed)
    
    prompt.run(args.API)
    
    prompt.save(args.saveFile)
