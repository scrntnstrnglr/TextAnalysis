import os
import sys
import csv

class TwitterManager:
    tweets_list=[]
    tweet_tokens=[]
    def __init__(self,data_file):
        self.load_data(data_file)
    
    def load_data(self,data_file):
        self.tweet_tokens=[]
        self.tweets_list=[]
        with open(data_file,encoding="utf8") as csv_file:
            csv_reader=csv.DictReader(csv_file,delimiter=',')
            line_count=0
            for row in csv_reader:
                self.tweets_list.append(row["text"])

    def get_tweets_list(self):
        return self.tweets_list

    def tokenize(self,tweets_list):
        for tweet in tweets_list:
            self.tweet_tokens.append(tweet.split())
        return self.tweet_tokens



def main():
    cwd=os.getcwd()
    obj = TwitterManager('C:\\Users\\SIDDHARTHA\\Trinity\\TextAnalysis\\TextAnalysis\\Sentimentalysis\\tweets_after.csv')
    tweets_list=obj.get_tweets_list()
    print(len(tweets_list))
    #tweets_tokens=obj.tokenize(tweets_list)

if __name__ == '__main__':
    main()
