from TwitterManager import TwitterManager
from progressbar import ProgressBar
import json
from matplotlib.colors import Normalize
import matplotlib.cm as cm
from Lexicon import Lexicon
from nltk import FreqDist, classify, NaiveBayesClassifier
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.corpus import twitter_samples, stopwords
import nltk
import re
import string
import random,os
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
import pathlib
nltk.download('twitter_samples')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
import random
import operator
import pandas as pd
root_path = pathlib.Path(__file__).parents[1]
from IPython.display import display

def lemmatize_sentence(tokens):
    '''
    lemmatizing words, for e.g 'run', 'ran', 'running' is the same word.
    The lemmatizer conforms similar words to an equivalent form, or is transformed to its root form
    '''
    lemmatizer = WordNetLemmatizer()
    lemmatized_sentence = []
    for word, tag in pos_tag(tokens):
        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        lemmatized_sentence.append(lemmatizer.lemmatize(word, pos))
    return lemmatized_sentence


def remove_noise(tweet_tokens, stop_words=()):
    '''
    Removing stop words like 'is', 'the' etc. lemmatize_sentence() function implementation is 
    reused here.
    '''
    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', token)
        token = re.sub("(@[A-Za-z0-9_]+)", "", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens


def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token


def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)


def plot_overall_count(before_count, after_count):
    fig = plt.figure()
    tweet_type = ['After', 'Before']
    tweet_counts = [after_count, before_count]
    ax = fig.add_axes([0, 0, 1, 1])
    ax.bar(tweet_type, tweet_counts)
    name='overall.png'
    plt.savefig(os.path.join(root_path,'plots',name), bbox_inches="tight")


def plot_emotion_graphs(emotions_after, emotions_before, name):
    emotions_colors = {'anger': 'red', 'anticipation': 'purple', 'disgust': 'yellow', 'fear': 'indigo', 'joy': 'green',
                       'against': 'black', 'for': 'pink', 'sadness': 'blue', 'surprise': 'maroon', 'trust': 'orange', 'unclassified': 'cyan'}


    total = sum(emotions_after.values())
    for key in emotions_after:
        percent=(emotions_after[key]/total)*100
        emotions_after[key]=percent

    total = sum(emotions_before.values())
    for key in emotions_before:
        percent=(emotions_before[key]/total)*100
        emotions_before[key]=percent

    #labels = list(emotions_colors.keys())
    #handles = [plt.Rectangle((1,1),1,1, color=emotions_colors[label]) for label in labels]
    my_cmap = cm.get_cmap('jet')
    ind = np.arange(len(emotions_after))
    width = 0.3
    fig = plt.figure(num=None, figsize=(10, 6), dpi=80,facecolor='w', edgecolor='k')
    fig.suptitle('Emotional Analysis of tweets for '+name, fontsize=16)
    ax = fig.add_subplot(111)
    pos_bars = ax.bar(ind, list(emotions_before.values()),width, color='g', align='center')
    neg_bars = ax.bar(ind+width, list(emotions_after.values()),width, color='r', align='center')
    ax.set_ylabel('% age')
    ax.set_xticklabels(list(emotions_after.keys()), rotation=90)
    ax.set_xticks(ind+width/2)
    ax.legend((pos_bars[0], neg_bars[0]), ('Before', 'After'))


    def autolabel(bars):
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x()+bar.get_width()/2., 1.05*h, '%.1f'%float(h),ha='center', va='bottom')


    autolabel(pos_bars)
    autolabel(neg_bars)

    name=name+'.png'
    plt.savefig(os.path.join(root_path,'plots',name), bbox_inches="tight")


def main():
    
    #twitterati = TwitterManager('C:\\Users\\SIDDHARTHA\\Trinity\\TextAnalysis\\TextAnalysis\\GetOldTweets3\\Test Datasets')
    #all_tweets = twitterati.get_tweets()
    #all_tweets_tokens = twitterati.get_tweet_tokens()
    #print(all_tweets)
    #print(all_tweets_tokens)
    #loading previous
    with open('allhashtagsjson.json') as f:
        previous_data = json.load(f)
    #print(previous_data)

    
    df = pd.read_csv('C:/Users/SIDDHARTHA/Trinity/TextAnalysis/TextAnalysis/GetOldTweets3/Datasets/Generic Hashtags/hashtags_past_six_months_tweets.csv')
    all_tweets_tokens = {'all_tweets' : {}}
    for index, row in df.iterrows():
        print(index)
        datetime = str(row['date'])
        datetime = datetime[:datetime.find(" ")]
        text = str(row['text'])
        if datetime not in previous_data:
            if datetime in all_tweets_tokens.get('all_tweets'):
                datetimelist = all_tweets_tokens.get('all_tweets').get(datetime)
                datetimelist.append(text.split())
                all_tweets_tokens.get('all_tweets')[datetime] = datetimelist
            else:
                all_tweets_tokens.get('all_tweets')[datetime] = [text.split()]
    
    #print(all_tweets_tokens.get('all_tweets'))
    print("DataSet created...")
    print(len(all_tweets_tokens.get('all_tweets')))
    limit=1500  #limit for parties=1500, rb=740,hashtags=11000
    #print('Total comparable entities: ',len(all_tweets))
    total_tweets={}
    emotions_count_dict_datetime = {}
    
    for datetime in all_tweets_tokens.get('all_tweets').keys():    
        #print(f'Running for {datetime}')
        emotions_count_dict={"anger": 0,"anticipation": 0,"disgust": 0,"fear": 0,"joy": 0,"against": 0,"for": 0,"sadness": 0,"surprise": 0,"trust": 0,"unclassified": 0}
        tweets = all_tweets_tokens.get('all_tweets')[datetime]
        #print('Before cleaning:: %s has %d tweets' %(datetime,len(tweets)))
        tweets_no_dup = []
        [tweets_no_dup.append(x) for x in tweets if x not in tweets_no_dup] 
        tweets=tweets_no_dup
        print('After removing duplicates:: %s has %d tweets' %(datetime,len(tweets)))
        
        #total_tweets[item+"_after"]=len(after_tweets)
        #total_tweets[item+"_before"]=len(before_tweets)

        #Cleaning tokens
        
        cleaned_tokens_list = []
        stop_words = stopwords.words('english')
        print("Cleaning tokens....")
        for tokens in tweets:
            cleaned_tokens_list.append(remove_noise(tokens, stop_words))

        #print(cleaned_tokens_list)
        tokens_for_model = get_tweets_for_model(cleaned_tokens_list)
        
        
        emotion_fetcher = Lexicon("C:/Users/SIDDHARTHA/Trinity/TextAnalysis/TextAnalysis/Sentimentalysis/NRC-Sentiment-Emotion-Lexicons/NRC-Sentiment-Emotion-Lexicons/NRC-Emotion-Lexicon-v0.92/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt")
        emotions_count_dict_after = {"anger":0,"anticipation":0,"disgust":0,"fear":0,"joy":0,"against":0,"for":0,"sadness":0,"surprise":0,"trust":0,"unclassified":0}

        #print("Creating count for after tweets...")
        pos_count=0
        emotions_list=[]
        pos_word_list=[]
        for i,tweet_dict in enumerate(tokens_for_model):
            #print(f'Running analysis {i}')
            sent_dict={"anger": 0,"anticipation": 0,"disgust": 0,"fear": 0,"joy": 0,"against": 0,"for": 0,"sadness": 0,"surprise": 0,"trust": 0,"unclassified": 0}
            for word,tag in pos_tag(tweet_dict):
                for sentiment in emotion_fetcher.get_emotion(word):
                    sent_dict[sentiment]+=1
            #del sent_dict['anger']
            #del sent_dict['anticipation']
            #del sent_dict['disgust']
            #del sent_dict['fear']
            #del sent_dict['joy']
            del sent_dict['against']
            del sent_dict['for']
            #del sent_dict['sadness']
            #del sent_dict['surpirse']
            #del sent_dict['trust']
            del sent_dict['unclassified']
            #print('Finding max...')
            max_sent=max(sent_dict.items(), key=operator.itemgetter(1))[0]
            emotions_count_dict[max_sent]+=1
            #pos_count+=1
        print('Updating dictionary...')
        emotions_count_dict_datetime[datetime] = emotions_count_dict
        print('Dictionary updated ...')
    print(emotions_count_dict_datetime)
    with open('allhashtagsjson_new.json','w') as f:
        json.dump(emotions_count_dict_datetime, f)

    x = list(emotions_count_dict_datetime.keys())
    anger,aniticipation,disgust,fear,joy,against,_for,sadness,surprise,trust,unclassified=[],[],[],[],[],[],[],[],[],[],[]
    for emo_dict in emotions_count_dict_datetime.values():
        anger.append(emo_dict.get('anger'))
        aniticipation.append(emo_dict.get('aniticipation'))
        disgust.append(emo_dict.get('disgust'))
        fear.append(emo_dict.get('fear'))
        joy.append(emo_dict.get('joy'))
        against.append(emo_dict.get('against'))
        _for.append(emo_dict.get('_for'))
        sadness.append(emo_dict.get('sadness'))
        surprise.append(emo_dict.get('surprise'))
        trust.append(emo_dict.get('trust'))
        unclassified.append(emo_dict.get('unclassified'))
    x=np.array(x)
    plt.plot(x, np.array(anger), 'r--', x, np.array(disgust), 'b--', x, np.array(sadness), 'g--')
    plt.show()
    
if __name__ == '__main__':
    main()
