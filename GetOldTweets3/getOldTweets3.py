#https://pypi.org/project/GetOldTweets3/
#https://github.com/Mottl/GetOldTweets3#egg=GetOldTweets3


#FOR HELP:
#    %run bin/GetOldTweets3 -h
#    %run bin/GetOldTweets3 --username "iamsrk" --maxtweets 10


import GetOldTweets3 as got
import sys
import traceback

start_date_before = "2020-01-08"
end_date_before = "2020-02-09"

start_date_after = "2020-02-09"
end_date_after = "2020-03-01"

language = "en"
emoji = "unicode"
maxtweets = 5000

before_after_list = ["before", "after"];

candidates_dict = {
#        "Richard_Bruton": ["@RichardbrutonTD", "Richard Bruton"],
#        "Mary_Lou_McDonald": ["@MaryLouMcDonald","Mary Lou McDonald"],
#        "Leo_Varadkar": ["@LeoVaradkar", "Leo Varadkar"],
#
#        "Fine_Gael": ["#finegael", "@FineGael"],
#        "Fianna_Fáil": ["#fiannafail", "@fiannafailparty"],
#        "Sinn_Féin": ["#sinnfein", "@sinnfeinireland"],
#        "Green_Party": ["#greenparty", "@greenparty_ie"],
#        "Labour": ["#labour", "@labour"],
#        "Social_Democrats": ["#socdem", "@SocDems"],
#        "Solidarity_People_Before_Profit": ["#pb4p", "@pb4p"]

#        "Hashtags": ["#ge2020", "#ge20", "#generalelections2020", "#leadersdebate", #generalelection2020", "#generalelection" ],
}

#before = True
before = False

for key, values in candidates_dict.items():
    if(before):
        outputFileName = key.lower() +"_before.csv"
        startDate = start_date_before
        endDate = end_date_before
    else:
        outputFileName = key.lower() +"_after.csv"
        startDate = start_date_after
        endDate = end_date_after

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
                                                        .setSince(startDate)\
                                                        .setUntil(endDate)\
                                                        .setMaxTweets(maxtweets)\
                                                        .setLang(language)\
                                                        .setEmoji(emoji)

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