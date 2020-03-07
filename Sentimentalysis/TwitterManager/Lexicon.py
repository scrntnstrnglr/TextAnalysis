# -*- coding: utf-8 -*-
"""

"""

import os
import sys

class Lexicon:
    emotions_dict = {"anger":[],"anticipation":[],"disgust":[],"fear":[],"joy":[],"against":[],"for":[],"sadness":[],"surprise":[],"trust":[],"unclassified":[]}
    emotions_count_dict = {"anger":0,"anticipation":0,"disgust":0,"fear":0,"joy":0,"against":0,"for":0,"sadness":0,"surprise":0,"trust":0,"unclassified":0}
    def __init__(self,emo_word_file):
        cwd = os.getcwd()
        self._load_emotions(emo_word_file)

    def _load_emotions(self,emo_word_file):
        emotions_file = open(emo_word_file,'r')
        lines = emotions_file.readlines()
        count=0
        for line in lines:
            thisLineList=line.strip().split()
            if(thisLineList[2]!='0'):
                self.emotions_dict[thisLineList[1]].append(thisLineList[0])

    def get_emotion(self,word):
        thisWordEmotions = []
        for sentiment in self.emotions_dict:
            if(word in self.emotions_dict[sentiment]):
                thisWordEmotions.append(sentiment)

        
        return thisWordEmotions

    def get_emotions_count_dict(self,word):
        return self.emotions_count_dict




def main():
    cwd=os.getcwd()
    obj = Lexicon("C:/Users/SIDDHARTHA/Trinity/TextAnalysis/TextAnalysis/Sentimentalysis/NRC-Sentiment-Emotion-Lexicons/NRC-Sentiment-Emotion-Lexicons/NRC-Emotion-Lexicon-v0.92/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt")
    print(obj.get_emotion("shout"))
    print(obj.get_emotions_count_dict("shout"))

if __name__ == '__main__':
    main()