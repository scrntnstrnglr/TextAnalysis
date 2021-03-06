import os
import sys
import csv
import json
import pathlib
from progressbar import ProgressBar

class TwitterManager:
    tweets_list=[]
    tweet_tokens=[]
    tweet_list_dict={}
    tweet_token_dict={}
    root_path = pathlib.Path(__file__).parents[1]
    def __init__(self,data_file_dir,name=None):
        self.load_data(data_file_dir,name)

    def create_data_structure(self,this_files):
        file_names=[]
        data_structure={}
        for item in this_files:
           name=item[:item.rindex('_')]
           if name not in file_names:
               file_names.append(name)
               data_structure[name] = {} 
               data_structure[name]['after'] = []
               data_structure[name]['before'] = []
        return data_structure

    def load_data(self,data_file_dir,name):
        this_file_dict={}
        this_tokens_dict={}
        files=[]
        for (dirpath, dirnames, filenames) in os.walk(data_file_dir):
            files.extend(filenames)
        
        if name is not None:
            this_files = [i for i in files if i.startswith(name)]
        else:
            this_files = files

        self.tweet_list_dict=self.create_data_structure(this_files)
        self.tweet_token_dict=self.create_data_structure(this_files)

        pbar=ProgressBar()
        print("Reading files....")
        for csv_file in pbar(this_files):
            this_tweets=[]
            this_tweet_tokens = []
            this_file_name=csv_file[:csv_file.rindex('_')]
            seqs=csv_file.split('_')
            seq=seqs[len(seqs)-1]
            this_file_seq=seq.split('.')[0]
            this_tweets=self.create_tweets_list(os.path.join(data_file_dir,csv_file))
            self.tweet_list_dict[this_file_name][this_file_seq]=this_tweets
            this_tweet_tokens=self.tokenize(this_tweets)
            self.tweet_token_dict[this_file_name][this_file_seq] = this_tweet_tokens
        
    
    def create_tweets_list(self,data_file):
        self.tweet_tokens=[]
        self.tweets_list=[]
        with open(data_file,encoding="utf8") as csv_file:
            csv_reader=csv.DictReader(csv_file,delimiter=',')
            line_count=0
            for row in csv_reader:
                self.tweets_list.append(row["text"])
        return self.tweets_list

    def get_tweets(self,name=None,seq=None):
        if name is None and seq is None:
            return self.tweet_list_dict
        if name is not None and seq is None:
            return self.tweet_list_dict[name]
        if name is not None and seq is not None:
            return self.tweet_list_dict[name][seq]

    def get_tweet_tokens(self,name=None,seq=None):
        if name is None and seq is None:
            return self.tweet_token_dict
        if name is not None and seq is None:
            return self.tweet_token_dict[name]
        if name is not None and seq is not None:
            return self.tweet_token_dict[name][seq]


    def tokenize(self,tweets_list):
        for tweet in tweets_list:
            self.tweet_tokens.append(tweet.split())
        return self.tweet_tokens

    def dump_to_json(self,dir,file_name,data):
        print('Writing data to json for ',file_name)
        with open(os.path.join(self.root_path,dir,file_name), 'w') as outfile:
            json.dump(data, outfile)

def main():
    cwd=os.getcwd()
    obj = TwitterManager('C:\\Users\\SIDDHARTHA\\Trinity\\TextAnalysis\\TextAnalysis\\GetOldTweets3\\testdatasets')
    #tweets_list=obj.get_tweets_list()
    #print(len(tweets_list))
    #tweets_tokens=obj.tokenize(tweets_list)

if __name__ == '__main__':
    main()