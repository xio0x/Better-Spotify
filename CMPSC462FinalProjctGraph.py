################################################################################
# Program name: CMPSC462FinalProjectGraph
#
# Author: Aram Asdourian
#
# Date: 11/8/2025
#
# Description:
# this is the graph data structure made for the song player project
################################################################################
#importing spotipy and registering credentials
from importlib.util import find_spec

import spotipy
from redis.commands.search.querystring import intersect
from spotipy.oauth2 import SpotifyClientCredentials
client_id = 'd9c29b7112ee4515a994c95de11bcf6e'
client_secret = '5dd7d593c41b4082ad6f0f5fa671a208'
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
#got help with spotify api from spotify website: https://developer.spotify.com/documentation/web-api


################################################################################
# Class name: genreGraph
#
# Author: Aram Asdourian
#
# Date: 11/8/2025
#
# Description:
# this graph stores genres as nodes that point to the artist nodes within those genres
# it also has a reversegraph where artists point to their genres
#
# Methods:
#     init:
#         reads the data from data.txt to build the graph on initialization
#         all new nodes added to the graph are also added to data.txt so the graph grows with more use
#
#    addArtistByName:
#        takes the name of an artist and uses the spotify api to find the top result
#        the top result for the name is then added to the graph along with their genres
#
#    addArtistByID:
#        same as above but accepts ID instead (the jumble of letters&numbers at the end of a url for an artists spotify page)
#
#    addArtistManually:
#        accepts an artist name and a list of their genres to add to the graph without the use of the api
#
#    isArtistInGraph:
#        returns true if the artist is in the graph or false if the artist is not in the graph
#
#    findArtistsInGenre:
#        takes a genre as input and returns all artists in that genre
#
#    findGenresOfArtist:
#        takes artist name as input and returns a list of all their genres
#
#    findSimilar:
#        uses an algoithm to search through neighboring artists in agraph to tally up points-
#        based on how similar one artist is to another. it returns a dictionary sorted most to least similar where-
#        the keys are the names of similar artists and the values are the points they got
################################################################################
class genreGraph:
    def __init__(self):
        #genres point to artists
        self.graph = {}
        #artists point to genres
        self.reversegraph = {}

        #imports data into the graph
        graphData = open("data.txt", 'r')
        #iterates over each line in the file and splits it by comma
        #each line contains an artist name and the genres associated with them seperated by commas
        for line in graphData.readlines():
            line = line.replace('\n', '').split(",")

            #makes the artist point to their genres in the reverse graph
            self.reversegraph[line[0]] = line[1:]

            #now creates the main graph
            #iterates over each genre assigned to each artist
            for i in range(1, len(line)):
                genre = line[-i]
                #if the genre is already in the graph add the artist to the values
                if genre in self.graph:
                    self.graph[line[-i]] += [line[0]]
                #if the genre isnt in the graph yet, makes the artist the sole value
                elif genre not in self.graph:
                    self.graph[line[-i]] = [line[0]]
        graphData.close()

    #this method adds new artists to the graph by accepting the name of the artist as input
    #it uses the search function of the spotify api to get the top result and add that artist to the graph
    #it dosent add artists if they are already in the graph
    #if a genre isnt yet in the graph it automatically adds it along with the artist
    def addArtistByName(self, artistName):
        # got help with finding genre of artist from stack overflow: https://stackoverflow.com/questions/61624487/extract-artist-genre-and-song-release-date-using-spotipy
        # uses sp.search() to look up an artist by name, uses several keys to narrow the data down to just the arist ID
        artistID = sp.search(artistName)['tracks']['items'][0]['artists'][0]['external_urls']['spotify']
        # the artist ID can be used to get the genres of an artist using sp.artist()
        artistGenres = sp.artist(artistID)['genres']
        #uses the ID found from the top search to get the proper spelling for the artist name
        artistName = sp.artist(artistID)['name']

        #checks if the artist is already in the graph before continuing
        if self.isArtistInGraph(artistName) == True:
            return

        # opens the data file and writes the artist with their genres
        # this is so data can be written to the graph at the start of next run
        graphData = open("data.txt", 'a')
        graphData.write("\n" + artistName + "," + ",".join(artistGenres))
        graphData.close()

        #finally adds the artist to the graph itself
        #iterates over each genre assigned to the artist
        for genre in artistGenres:
            # if the genre is already in the graph add the artist to the values
            if genre in self.graph:
                self.graph[genre] += [artistName]
            # if the genre isnt in the graph yet, makes the artist the sole value
            elif genre not in self.graph:
                self.graph[genre] = [artistName]

    #same as above but takes artist id as input instead
    def addArtistByID(self, artistID):
        #obtains the artist name from the id and checks if its already in the graph
        artistName = sp.artist(artistID)['name']

        #checks if the artist is already in the graph before continuing
        if self.isArtistInGraph(artistName) == True:
            return

        # the artist ID can be used to get the genres of an artist using sp.artist()
        artistGenres = sp.artist(artistID)['genres']

        # opens the data file and writes the artist with their genres
        # this is so data can be written to the graph at the start of next run
        graphData = open("data.txt", 'a')
        graphData.write("\n" + artistName + "," + ",".join(artistGenres))
        graphData.close()

        #finally adds the artist to the graph itself
        #iterates over each genre assigned to the artist
        for genre in artistGenres:
            # if the genre is already in the graph add the artist to the values
            if genre in self.graph:
                self.graph[genre] += [artistName]
            # if the genre isnt in the graph yet, makes the artist the sole value
            elif genre not in self.graph:
                self.graph[genre] = [artistName]


    #another alternate way to add artists to the graph
    #takes the name of an artist and the list of genres as input and adds them
    def addArtistManually(self,artistName,genreList):
        if self.isArtistInGraph(artistName) == True:
            return

        # opens the data file and writes the artist with their genres
        # this is so data can be written to the graph at the start of next run
        graphData = open("data.txt", 'a')
        graphData.write("\n" + artistName + "," + ",".join(genreList))
        graphData.close()

        # iterates over each genre assigned to the artist
        for genre in genreList:
            # if the genre is already in the graph add the artist to the values
            if genre in self.graph:
                self.graph[genre] += [artistName]
            # if the genre isnt in the graph yet, makes the artist the sole value
            elif genre not in self.graph:
                self.graph[genre] = [artistName]

    #takes name of artist as input and returns true if in graph or false if not in graph
    def isArtistInGraph(self, artistName):
        #checks if the artist is anywhere in the graph, also checks insensitive to case
        if artistName.lower() in [artist.lower() for artist in self.reversegraph.keys()]:
            return True
        else:
            return False

    #takes the name of a genre as input and returns a list of all artists in that genre as output
    def findArtistsInGenre(self, genre):
        return(self.graph[genre])

    #accepts an artist as input and returns a list of all their genres
    def findGenresOfArtist(self, artistName):
        return(self.reversegraph[artistName])

    #takes an artist as input and creates a dictionary that assigns a score to how similar an artist is to the input artist
    #the first call takes all genres of the input artist and adds +1 score to each artist that shares that genre
    #each new artist that is encountered is then also visited to look at all of their genres
    #(with the philosophy that their genres are similar to the input artist by 1 degree of seperation, then 2, then 3)
    def findSimilar(self, artistName):
        #if the artist dosent have a set genre in spotify then an empty dictionary is returned
        if self.findGenresOfArtist(artistName) == ['']:
            return {}

        #tallys the score of each artist
        score = {}
        #tracks which genres have been visited
        visited = set([])
        #tracks which artists are currently being visited
        currentLevel = [artistName]


        iteration = 1
        #does 4 passthroughs, each passthrough is 1 degree of seperation from the input artist
        # I tested random numbers and found 3 and 4 was the sweet spot to find related artists
        while iteration < 4:
            #tracks which artists will be visited next
            nextLevel = []
            #iterates over each artist in the current level
            #(it starts with the input artist then fills with artists that share genres)
            for similarArtist in currentLevel:
                #iterates over the genres of the similar artists (except the ones that have already been visited)
                for genre in set(self.findGenresOfArtist(similarArtist))-visited:
                    #iterates over artists that share that genre
                    for neighbor in self.graph[genre]:
                        #adds up the score
                        if neighbor in score:
                            #the score tallied is deminished each iteration
                            score[neighbor] += (1/iteration)
                        else:
                            score[neighbor] = (1/iteration)
                            nextLevel.append(neighbor)

                    #adds the visited genres to the visited set so they cant be visited again later
                    visited.add(genre)
            #sets the new current level and iterates
            currentLevel = nextLevel
            iteration +=1

        #removes the input artist from the dictionary,sorts from greatest to least, and returns the dictionary
        score.pop(artistName)
        #got help with dictionary sorting from geeksforgeeks: https://www.geeksforgeeks.org/python/sort-python-dictionary-by-value/
        score = {key: value for key, value in sorted(score.items(),key=lambda item: item[1], reverse=True)}
        return(score)