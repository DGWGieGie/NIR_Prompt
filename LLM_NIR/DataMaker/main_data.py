import argparse
from DataProcess import DP

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--header", default=1, type=int) # the csv including header?
    parser.add_argument("--ratingP", default="ml-25m/ratings.csv", type=str) # rating.csv path
    parser.add_argument("--movieP", default="ml-25m/movies.csv", type=str) # movies.csv
    parser.add_argument("--NIR", default=1, type=int) # is this next-item recommendations task?
    parser.add_argument("--filename", default="ml-25mNIR.json", type=str) # the path that json will be kept
    args = parser.parse_args()
    
    dp = DP(args.ratingP, args.movieP, args.header)
    dp.writeJson(args.filename, args.NIR)
    


    