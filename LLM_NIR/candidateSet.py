import utils
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity, pairwise_distances

def createMovieDict(data):
    """create movie dict

    Args:
        data (list): the data that contains user watched movies, rating

    Returns:
        dict: the movies dict
    """
    uiDict = {}
    index = 0
    for elem in data:
        movies = elem[0].split(' | ')
        for movie in movies:
            if movie not in uiDict:
                uiDict[movie] = index
                index +=1
    return uiDict


def getMatrix(data, uiDict, RATINGS=0):
    """create user matrix

    Args:
        data (list): the data that contains user watched movies, rating
        uiDict (dict): the movies dict
        RATINGS (int, optional): consider ratings. Defaults to 0.

    Returns:
        np.array: user matrix
    """
    userL = []
    for elem in data:
        itemHotL = [0 for i in range(len(uiDict))]
        movies = elem[0].split(' | ')
        if RATINGS:
            ratings = elem[1].split(' | ')
        
        for movieIndex in range(len(movies)):
            if RATINGS:
                itemHotL[uiDict[movies[movieIndex]]] = ratings[movieIndex]
            else:
                itemHotL[uiDict[movies[movieIndex]]] = 1
        userL.append(itemHotL)
    return np.array(userL)


def createMoviePopDict(data):
    """create movie popular dict

    Args:
        data (list): the data that contains user watched movies, rating

    Returns:
        dict: the movies popular dict
    """
    popMovieDict = {}
    for elem in data:
        movies = elem[0].split(' | ')
        for movie in movies:
            if movie not in popMovieDict:
                popMovieDict[movie] = 0
            popMovieDict[movie] += 1
    return popMovieDict

def cosineSimilarity(matrix):
    return pairwise_distances(matrix, metric="cosine")

def euclideanSimilarity(matrix):
    return pairwise_distances(matrix, metric="euclidean")

def jaccardSimilarity(matrix):
    return pairwise_distances(matrix, metric="jaccard")

def manhattanSimilarity(matrix):
    return pairwise_distances(matrix, metric="manhattan")

class Similarity:
    def __init__(self, matrix, metrics=[]) -> None:
        self.distances = []
        for metric in metrics:
            if metric == "cosine":
                self.distances.append(cosineSimilarity(matrix))
            elif metric == "euclidean":
                self.distances.append(euclideanSimilarity(matrix))
            elif metric == "jaccard":
                self.distances.append(jaccardSimilarity(matrix))
            elif metric == "manhattan":
                self.distances.append(manhattanSimilarity(matrix))
    
    def getSimilaritys(self, index):
        similaritys = []
        for distances in self.distances:
            similaritys.append(distances[index])
        return similaritys
    
    def getSimilaritysAll(self):
        return self.distances
    
    



class uiMatrix:    
    def __init__(self, filename, USER=1, RATING=0) -> None:
        self.uiData = utils.read_json(filename)
        self.uiDict = createMovieDict(self.uiData)
        self.USER = USER
        if USER:
            self.uiMatrix = getMatrix(self.uiData, self.uiDict, RATING)
        else:
            self.uiMatrix = getMatrix(self.uiData, self.uiDict, RATING).T
        
    
    def getCandidate(self, curIndex, similaritys, user_nums, size, TARGET=0):
        if self.USER:
            return self.userFilter(curIndex, similaritys, user_nums, size, TARGET)
        
        else:
            return self.itemFilter(curIndex, similaritys, user_nums, size, TARGET)
    
    def userFilter(self, curIndex, similaritys, user_nums, size, TARGET):
        candidateDict = {} 
        watchedMovies = self.uiData[curIndex][0].split(' | ')
        
        for similarity in similaritys:  
            sortedSimilarity = sorted(list(enumerate(similarity)), key=lambda x: x[-1])[:user_nums]
            dvdSim = sum([sim[-1] for sim in sortedSimilarity])
            for simIndex, simValue in sortedSimilarity:
                movieWeight = 1 - simValue * 1.0/dvdSim
                candidateMovies = self.uiData[simIndex][0].split(' | ')

                for movie in candidateMovies:
                    if movie not in watchedMovies:
                        if movie not in candidateDict:
                            candidateDict[movie] = 0.
                        candidateDict[movie] += movieWeight
                           
        candidate_pairs = list(sorted(candidateDict.items(), key=lambda x:x[-1], reverse=True))
        candidate_items = [e[0] for e in candidate_pairs][:size]
        if TARGET and self.uiData[curIndex][-1] not in candidate_items:
            candidate_items[-1] = self.uiData[curIndex][-1]
        return candidate_items
    
    def itemFilter(self, curIndex, similaritys, item_nums, size, TARGET):
        candidateDict = {}
        moviesL = [key for key in self.uiDict.keys()]
        watchedMovies = self.uiData[curIndex][0].split(' | ')
        for similarity in similaritys: 
            for watchedmovie in watchedMovies:
                sortedSimilarity = sorted(list(enumerate(similarity[self.uiDict[watchedmovie]])), key=lambda x: x[-1])[:item_nums]
                dvdSim = sum([sim[-1] for sim in sortedSimilarity])
                for simIndex, simValue in sortedSimilarity:
                    movieWeight = 1 - simValue * 1.0/dvdSim
                    s_item = moviesL[simIndex]
                    
                    if moviesL[simIndex] not in watchedMovies:
                        if moviesL[simIndex] not in candidateDict:
                            candidateDict[s_item] = 0.
                        candidateDict[s_item] += movieWeight
                        
        candidate_pairs = list(sorted(candidateDict.items(), key=lambda x:x[-1], reverse=True))
        candidate_items = [e[0] for e in candidate_pairs][:size]
        if TARGET and self.uiData[curIndex][-1] not in candidate_items:
            candidate_items[-1] = self.uiData[curIndex][-1]
        return candidate_items
    
    
    
        