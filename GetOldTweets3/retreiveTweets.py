#https://pypi.org/project/GetOldTweets3/
#https://github.com/Mottl/GetOldTweets3#egg=GetOldTweets3


#FOR HELP:
#    %run bin/GetOldTweets3 -h
#    %run bin/GetOldTweets3 --username "iamsrk" --maxtweets 10


import GetOldTweets3 as got
import sys
import traceback
from datetime import datetime, timedelta

#start_date_before = "2020-01-08"
#end_date_before = "2020-02-09"

#start_date_after = "2020-02-09"
#end_date_after = "2020-03-01"

#subtract the same number of timedelta days in since_date to the current timedelta days in until_date to
#set until_date to since_date
until_date = datetime.now() - timedelta(days = 165)
since_date = until_date - timedelta(days = 26)

until_date = until_date.strftime("%Y-%m-%d")
since_date = since_date.strftime("%Y-%m-%d")

language = "en"
emoji = "unicode"
#maxtweets = 5000

fileExtension = ".csv"

before_after_list = ["before", "after"];

candidates_dict = {

#        Canadidates Twitter Handles
#        Fine_Gael
#        "Richard_Bruton": ["@RichardbrutonTD", "Richard Bruton"],
#        "Catherine_Noone": ["@senatornoone", "Catherine Noone"],


#        Fianna_Fáil

#        Sinn_Féin

#        Green_Party

#        Aontú

#        Solidarity_People_Before_Profit

#        Labour

#        Party Twitter Handles
#        "Fine_Gael": ["#finegael", "@FineGael"],
        "Fianna_Fáil": ["#fiannafail", "@fiannafailparty"],
#        "Sinn_Féin": ["#sinnfein", "@sinnfeinireland"],
#        "Green_Party": ["#greenparty", "@greenparty_ie"],
#        "Labour": ["#labour", "@labour"],
#        "Social_Democrats": ["#socdem", "@SocDems"],
#        "Solidarity_People_Before_Profit": ["#pb4p", "@pb4p"]
#        "Aontú": ["#aontu", "@AontuIE"],

#        Hashtags
#        "Hashtags": ["#ge2020", "#ge20", "#generalelections2020", "#leadersdebate", #generalelection2020", "#generalelection" ],
}

#Toggle the before value for each of the candidates above to get the before and after datasets
#before = True
#before = False

for key, values in candidates_dict.items():
#    if(before):
#        outputFileName = key.lower() +"_before.csv"
#        startDate = start_date_before
#        endDate = end_date_before
#    else:
#        outputFileName = key.lower() +"_after.csv"
#        startDate = start_date_after
#        endDate = end_date_after

    outputFileName = key.lower() + fileExtension
    outputFile = open(outputFileName, "w+", encoding='utf-8-sig')
    outputFile.write('date,username,to,replies,retweets,text,mentions,hashtags,permalink\n')

    cnt = 0
    def receiveBuffer(tweets):
        global cnt
        for t in tweets:
            data = [t.date.strftime("%Y-%m-%d %H:%M:%S"),
                t.username,
                t.to or '',
                t.replies,
                t.retweets,
                '" '+t.text.replace('"','""')+' "',
                t.mentions,
                t.hashtags,
                t.permalink]
            data[:] = [i if isinstance(i, str) else str(i) for i in data]
            outputFile.write(','.join(data) + '\n')

        outputFile.flush()
        cnt += len(tweets)

        if sys.stdout.isatty():
            print("\rSaved %i"%cnt, end='', flush=True)
        else:
            print(cnt, end=' ', flush=True)

    try:
        print("Downloading tweets for... " + outputFileName)
        for value in values:
            tweetCriteria = got.manager.TweetCriteria().setQuerySearch(value)\
                                                        .setSince(since_date)\
                                                        .setUntil(until_date)\
                                                        .setLang(language)\
                                                        .setEmoji(emoji)
#                                                        .setMaxTweets(maxtweets)\

            tweets = got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer);

    except KeyboardInterrupt:
            print("\r\nInterrupted.\r\n")

    except Exception as err:
            print(traceback.format_exc())
            print(str(err))

    finally:
        if "outputFile" in locals():
            outputFile.close()
            print()
            print('Done. Output file generated "%s".' % outputFileName + '\n')