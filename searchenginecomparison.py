#!/usr/bin/python

import sys
import math
import itertools

from sets import Set

class QueryFile:
    'Contents of single query file'

    def __init__ (self,name):
        #print "Creating new object with name = %s" % (name)
        self.name = name
        self.googleQueryList = []
        self.bingQueryList = []
        self.askQueryList = []
        self.populateContents()

    def populateContents(self):
        f = open(self.name,"r");
        lines = f.readlines()
        isQuerySet = False
        currentSearchEngine = "Google"
        for line in lines:
            if (line == "\n"):
                continue
            #print "line = %s " % (line)
            if (-1 != line.find("Query:") and isQuerySet == False):
                #self.query = line.split(':')
             #   print "found query in line %s" % (line)


                queryTokens = line.split(':')
                #print "query is %s" % (self.query)
                self.query = queryTokens[1][:-1]
                isQuerySet = True
            elif (line[:-1] == "Google" or line[:-1] == "Bing" or line[:-1] == "Ask"):
                currentSearchEngine = line[:-1]
            elif (line != ""):
                if (currentSearchEngine == "Google"):
                    self.googleQueryList.append(line[:-1]);
                elif (currentSearchEngine == "Bing"):
                    self.bingQueryList.append(line[:-1]);
                elif (currentSearchEngine == "Ask"):
                    self.askQueryList.append(line[:-1]);
        f.close()

    def getQuery(self):
        return self.query

    def getGoogleQueryList(self):
        return self.googleQueryList

    def getBingQueryList(self):
        return self.bingQueryList

    def getAskQueryList(self):
        return self.askQueryList

    def getGoogleQuerySet(self):
        return set(self.googleQueryList)

    def getBingQuerySet(self):
        return set(self.bingQueryList)

    def getAskQuerySet(self):
        return set(self.askQueryList)

	GoogleQuerySet = getGoogleQueryList(self)
	BingQuerySet = getBingQuerySet(self)
	AskQuerySet = getAskQuerySet(self)

def calcJaccardSimilarity(set1,set2):
	jUnion = set1|set2
	jIntersection = set1&set2
	jSimilarity = float(len(jIntersection)) / len(jUnion)
	return jSimilarity

def isOrderLower(list, string1, string2):
    if list.index(string1)<list.index(string2):
        return True
    else:
        return False

def getKendallsTau(list1, list2, string1, string2):
    if(isOrderLower(list1,string1,string2) == isOrderLower(list2,string1,string2)):
        return 0;
    else:
        return 1;

def calcKendallsTau(list1,list2):
    s1 = set(list1)
    s2 = set(list2)
    commonlen = len(s1&s2)
    print "common length = " + str(commonlen)
    if (commonlen == 0):
        print "No common elements found"
        return 1
    elif (commonlen == 1):
        print "Only one common element found"
        return 0
    else:
        commonset = s1&s2
        print commonset
        combos = itertools.combinations(commonset, 2)
        usable_combos = []
        for e in combos:
                usable_combos.append(e)
        k = 0
        for pair in usable_combos:
            print "Pair string 1 = " + pair[0]
            print "Pair string 2 = " + pair[1]
            k +=getKendallsTau(list1, list2, pair[0],pair[1])
            print "current Tau = " + str(k)

        norm = float(commonlen*(commonlen-1))/2;
        print "norm = " + str(norm)
        return float(k)/norm

def getSpearmansFootruleDistance(commonset, list1, list2):
    sfd = 0
    for element in commonset:
        sfd += math.fabs(list1.index(element)-list2.index(element))

    norm =0
    n = len(commonset)
    if (n%2 == 0):
        norm = float(n*n)/2
    else:
        norm = float(n+1)*(n-1)/2;

    return sfd/norm;

def calcSpearmansFootruleDistance(list1, list2):
    s1 = set(list1)
    s2 = set(list2)
    commonlen = len(s1&s2)
    print "common length = " + str(commonlen)
    if (commonlen == 0):
        print "No common elements found"
        return 1
    elif (commonlen == 1):
        print "Only one common element found"
        return 0
    else:
        commonset = s1&s2
        print commonset
        list1copy = list1
        list2copy = list2
        for element in list1copy:
            if element not in commonset:
                list1copy.remove(element)
        for element in list2copy:
            if element not in commonset:
                list2copy.remove(element)
        return getSpearmansFootruleDistance(commonset,list1copy, list2copy)




queryResultList = []
for i in range(1,11):
    fileName = "Q" + (("0"+str(i)) if (i<10) else str(i)) + "-results.txt"
    queryResultList.append(QueryFile(fileName))

tGoogle = 0
tBing = 0
tAsk = 0
tGB = 0
tGA = 0
tBA = 0
tGBA = 0
tAll = 0
pOne = 0
pTwo = 0
pThree =0

totalGoogleSet = set()
totalBingSet = set()
totalAskSet = set()

for i in range(len(queryResultList)):
    query = queryResultList[i].getQuery()
    print "Current Query is " + query
    iGoogle = len(queryResultList[i].getGoogleQuerySet()-(queryResultList[i].getBingQuerySet()|queryResultList[i].getAskQuerySet()))
    print "# Unique Google results only =" + str(iGoogle)
    tGoogle += iGoogle;
    iBing = len(queryResultList[i].getBingQuerySet()-(queryResultList[i].getGoogleQuerySet()|queryResultList[i].getAskQuerySet()))
    print "# Unique Bing results only =" + str(iBing)
    tBing += iBing
    iAsk = len(queryResultList[i].getAskQuerySet()-(queryResultList[i].getGoogleQuerySet()|queryResultList[i].getBingQuerySet()))
    print "# Unique Ask results only =" + str(iAsk)
    tAsk += iAsk
    iGB = len((queryResultList[i].getGoogleQuerySet() & queryResultList[i].getBingQuerySet())-queryResultList[i].getAskQuerySet())
    print "# Unique Google and Bing only =" + str(iGB)
    tGB += iGB
    iGA = len((queryResultList[i].getGoogleQuerySet() & queryResultList[i].getAskQuerySet())-queryResultList[i].getBingQuerySet())
    print "# Unique Google and Ask only =" + str(iGA)
    tGA += iGA
    iBA = len((queryResultList[i].getBingQuerySet() & queryResultList[i].getAskQuerySet())-queryResultList[i].getGoogleQuerySet())
    print "# Unique Bing and Ask only =" + str(iBA)
    tBA += iBA
    iGBA = len(queryResultList[i].getGoogleQuerySet() & queryResultList[i].getBingQuerySet() & queryResultList[i].getAskQuerySet())
    print "# Unique All three search engines only=" + str(iGBA)
    tGBA += iGBA
    iAll = len(queryResultList[i].getGoogleQuerySet()|queryResultList[i].getBingQuerySet()|queryResultList[i].getAskQuerySet())
    print "# All three search engines =" + str(iAll)
    tAll += iAll
    pOne = float(iGoogle+iBing+iAsk)*100/iAll
    print "# Percentage of unique results returned by one search engine =" + str(pOne)
    pTwo = float(iGB+iGA+iBA)*100/iAll
    print "# Percentage of unique results returned by two search engines =" + str(pTwo)
    pThree = float(iGBA)*100/iAll
    print "# Percentage of unique results returned by all three search engines =" + str(pThree)

    # Calculating Jaccard Similarity
    print "Jaccard Similarity between Google and Bing = " + str(calcJaccardSimilarity(queryResultList[i].getGoogleQuerySet(),queryResultList[i].getBingQuerySet()))

    print "Jaccard Similarity between Google and Ask = " + str(calcJaccardSimilarity(queryResultList[i].getGoogleQuerySet(),queryResultList[i].getAskQuerySet()))

    print "Jaccard Similarity between Bing and Ask = " + str(calcJaccardSimilarity(queryResultList[i].getBingQuerySet(),queryResultList[i].getAskQuerySet()))

    totalGoogleSet |= queryResultList[i].getGoogleQuerySet()
    totalBingSet |= queryResultList[i].getBingQuerySet()
    totalAskSet |= queryResultList[i].getAskQuerySet()

    # Calculate Kendalls Tau
    print "Kendall's Tau between Google and Bing = " + str(calcKendallsTau(queryResultList[i].getGoogleQueryList(),queryResultList[i].getBingQueryList()))
    print "Kendall's Tau between Google and Ask = " + str(calcKendallsTau(queryResultList[i].getGoogleQueryList(),queryResultList[i].getAskQueryList()))
    print "Kendall's Tau between Bing and Ask = " + str(calcKendallsTau(queryResultList[i].getBingQueryList(),queryResultList[i].getAskQueryList()))

    # Calculate Spearmans Footrule Distance
    print "Spearman's Footrule Distance between Google and Bing = " + str(calcSpearmansFootruleDistance(queryResultList[i].getGoogleQueryList(),queryResultList[i].getBingQueryList()))
    print "Spearman's Footrule Distance between Google and Ask = " + str(calcSpearmansFootruleDistance(queryResultList[i].getGoogleQueryList(),queryResultList[i].getAskQueryList()))
    print "Spearman's Footrule Distance between Bing and Ask = " + str(calcSpearmansFootruleDistance(queryResultList[i].getBingQueryList(),queryResultList[i].getAskQueryList()))

print "Total # Unique Google results only =" +  str(tGoogle)
print "Total # Unique Bing results only =" + str(tBing)
print "Total # Unique Ask results only =" + str(tAsk)
print "Total # Unique Google and Bing only =" + str(tGB)
print "Total # Unique Google and Ask only =" + str(tGA)
print "Total # Unique Bing and Ask only =" + str(tBA)
print "Total # Unique All three search engines only =" + str(tGBA)
print "Total # All three search engines =" + str(tAll)
pOneOverall = float(tGoogle+tBing+tAsk)*100/tAll;
pTwoOverall = float(tGB+tGA+tBA)*100/tAll;
pThreeOverall = float(tGBA)*100/tAll;
print "Total # Percentage of unique results returned by one search engine =" + str(pOneOverall)
print "Total # Percentage of unique results returned by two search engines =" + str(pTwoOverall)
print "Total # Percentage of unique results returned by three search engines =" + str(pThreeOverall)

print "Overall Jaccard Similarity between Google and Bing = " + str(calcJaccardSimilarity(totalGoogleSet,totalBingSet))
print "Overall Jaccard Similarity between Google and Ask = " + str(calcJaccardSimilarity(totalGoogleSet,totalAskSet))
print "Overall Jaccard Similarity between Bing and Ask = " + str(calcJaccardSimilarity(totalBingSet,totalAskSet))


