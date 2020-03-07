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
root_path = pathlib.Path(__file__).parents[1]

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
    
    twitterati = TwitterManager('C:\\Users\\SIDDHARTHA\\Trinity\\TextAnalysis\\TextAnalysis\\GetOldTweets3\\AllCandidates')
    all_tweets = twitterati.get_tweets()
    all_tweets_tokens = twitterati.get_tweet_tokens()
    limit=1500  #limit for parties=1500, rb=740,hashtags=11000
    print('Total comparable entities: ',len(all_tweets))
    total_tweets={}
    pbar=ProgressBar()
    for item in pbar(all_tweets_tokens.keys()):
        after_tweets = all_tweets_tokens[item]['after']
        before_tweets = all_tweets_tokens[item]['before']
        print('Before cleaning:: %s has %d tweets after the election and %d tweets before the election' %(item,len(after_tweets),len(before_tweets)))
        after_tweets_no_dup = []
        before_tweets_no_dup = []
        [after_tweets_no_dup.append(x) for x in after_tweets if x not in after_tweets_no_dup] 
        [before_tweets_no_dup.append(x) for x in before_tweets if x not in before_tweets_no_dup] 
        after_tweets=after_tweets_no_dup
        before_tweets=before_tweets_no_dup
        print('After cleaning:: %s has %d tweets after the election and %d tweets before the election' %(item,len(after_tweets),len(before_tweets)))
        total_tweets[item+"_after"]=len(after_tweets)
        total_tweets[item+"_before"]=len(before_tweets)
        '''
        print('Randomizing.....')
        if len(after_tweets)>limit: 
            after_tweets=random.sample(after_tweets,limit)
        if len(before_tweets)>limit:
            before_tweets=random.sample(before_tweets,limit)

        print('After randomizing:: %s has %d tweets after the election and %d tweets before the election' %(item,len(after_tweets),len(before_tweets)))
        '''
        #Cleaning tokens
        
        after_cleaned_tokens_list = []
        before_cleaned_tokens_list = []
        stop_words = stopwords.words('english')
        print("Cleaning after tokens....")
        pbar1 = ProgressBar()
        for tokens in pbar1(after_tweets):
            after_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

        print("Cleaning before tokens....")
        pbar2 = ProgressBar()
        for tokens in pbar2(before_tweets):
            before_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

        
        after_tokens_for_model = get_tweets_for_model(after_cleaned_tokens_list)
        before_tokens_for_model =get_tweets_for_model(before_cleaned_tokens_list)

        emotion_fetcher = Lexicon("C:/Users/SIDDHARTHA/Trinity/TextAnalysis/TextAnalysis/Sentimentalysis/NRC-Sentiment-Emotion-Lexicons/NRC-Sentiment-Emotion-Lexicons/NRC-Emotion-Lexicon-v0.92/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt")
        emotions_count_dict_after = {"anger":0,"anticipation":0,"disgust":0,"fear":0,"joy":0,"against":0,"for":0,"sadness":0,"surprise":0,"trust":0,"unclassified":0}

        print("Creating count for after tweets...")
        pos_count=0
        emotions_list=[]
        pos_word_list=[]
        for tweet_dict in after_tokens_for_model:
            sent_dict={"anger": 0,"anticipation": 0,"disgust": 0,"fear": 0,"joy": 0,"against": 0,"for": 0,"sadness": 0,"surprise": 0,"trust": 0,"unclassified": 0}
            for word,tag in pos_tag(tweet_dict):
                for sentiment in emotion_fetcher.get_emotion(word):
                    sent_dict[sentiment]+=1
            del sent_dict['anger']
            del sent_dict['anticipation']
            del sent_dict['disgust']
            del sent_dict['fear']
            #del sent_dict['joy']
            #del sent_dict['against']
            #del sent_dict['for']
            del sent_dict['sadness']
            #del sent_dict['surpirse']
            #del sent_dict['trust']
            del sent_dict['unclassified']
            max_sent=max(sent_dict.items(), key=operator.itemgetter(1))[0]
            emotions_count_dict_after[max_sent]+=1
            pos_count+=1
        
        print(emotions_count_dict_after)
        dump_file_name="emotions_"+item+"_after.json"
        twitterati.dump_to_json('jsons',dump_file_name,emotions_count_dict_after)
        print(pos_count)


        #-----------------------------------------------------------------------------------

        
        emotions_count_dict_before = {"anger":0,"anticipation":0,"disgust":0,"fear":0,"joy":0,"against":0,"for":0,"sadness":0,"surprise":0,"trust":0,"unclassified":0}
        print("Creating count for before tweets...")
        neg_count=0
        emotions_list=[]
        neg_word_list=[]
        for tweet_dict in before_tokens_for_model:
            sent_dict={"anger": 0,"anticipation": 0,"disgust": 0,"fear": 0,"joy": 0,"against": 0,"for": 0,"sadness": 0,"surprise": 0,"trust": 0,"unclassified": 0}
            for word,tag in pos_tag(tweet_dict):
                for sentiment in emotion_fetcher.get_emotion(word):
                    sent_dict[sentiment]+=1
            del sent_dict['anger']
            del sent_dict['anticipation']
            del sent_dict['disgust']
            del sent_dict['fear']
            #del sent_dict['joy']
            #del sent_dict['against']
            #del sent_dict['for']
            del sent_dict['sadness']
            #del sent_dict['surpirse']
            #del sent_dict['trust']
            del sent_dict['unclassified']
            max_sent=max(sent_dict.items(), key=operator.itemgetter(1))[0]
            emotions_count_dict_before[max_sent]+=1
            neg_count+=1


        print(emotions_count_dict_before)
        dump_file_name="emotions_"+item+"_before.json"
        twitterati.dump_to_json('jsons',dump_file_name,emotions_count_dict_before)
        print(neg_count)
    

        #removing for and against keys from dict.
        del emotions_count_dict_after['anger']
        del emotions_count_dict_after['anticipation']
        del emotions_count_dict_after['disgust']
        del emotions_count_dict_after['fear']
        #del emotions_count_dict_after['joy']
        #del emotions_count_dict_after['against']
        #del emotions_count_dict_after['for']
        del emotions_count_dict_after['sadness']
        #del emotions_count_dict_after['surpirse']
        #del emotions_count_dict_after['trust']
        del emotions_count_dict_after['unclassified']

        del emotions_count_dict_before['anger']
        del emotions_count_dict_before['anticipation']
        del emotions_count_dict_before['disgust']
        del emotions_count_dict_before['fear']
        #del emotions_count_dict_before['joy']
        #del emotions_count_dict_before['against']
        #del emotions_count_dict_before['for']
        del emotions_count_dict_before['sadness']
        #del emotions_count_dict_before['surpirse']
        #del emotions_count_dict_before['trust']
        del emotions_count_dict_before['unclassified']

        #plot_overall_count(pos_count, neg_count)
        plot_emotion_graphs(emotions_count_dict_after,emotions_count_dict_before,item)
        print('total tweets:')
        print(total_tweets)
        print("--------------------------------------------------------------------------------\n")
        
if __name__ == '__main__':
    main()
