import time
import math
from _datetime import datetime
import tweepy
from tweepy import OAuthHandler

import couchdb


#our key to twitter API
consumer_key = 'XsIT8AInFpWzKOxqxxUGIyjUF'
consumer_secret = 'SqJchyijqas6re8YCGhHDhm9QgAe2DOYPhnQQGF2YLXFc8NNED'
access_token = '1128155636858904576-Na27CLWShUdxbkRVMmnGgnsiLifdKV'
access_secret = 'aTsFpIIyFrFX8Tyk2F95KzU1y5KVUM0gVgAO9E3j9Y49w'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

db_host = "http://admin:admin@45.113.233.247:5984"
# db_host = "http://ailinz1:unimelb666@localhost:5984"
couch = couchdb.Server(db_host)


# db_name is a string
def save_to_db(data, db_name):
    try:
        db = couch[db_name]
    except:
        db = couch.create(db_name)
    db.update(data)

def update_informationsdb(data, doc_id):
    try:
        db = couch["informations"]
    except:
        db = couch.create("informations")
    try:
        doc = db.get(doc_id)
        doc['tweets'] = data['tweets']
        doc['following'] = data['following']
        doc['followers'] = data['followers']
        doc['likes'] = data['likes']
    except:
        db.save(data)

def get_usr_information(sch_id, sch_name):
    print("Updating information for ", sch_name, " ...")
    raw = api.get_user(sch_id)
    new_data = {}
    new_data['_id'] = sch_name
    new_data['name'] = raw._json['name']
    new_data['tweets'] = raw._json['statuses_count']
    new_data['following'] = raw._json['friends_count']
    new_data['followers'] = raw._json['followers_count']
    new_data['likes'] = raw._json['favourites_count']
    new_data['description'] = raw._json['description']
    new_data['url'] = raw._json['url']
    update_informationsdb(new_data, sch_name)


def get_update_time(database):
    total_count = 0
    max_id = 00000000000000000000000000000000
    min_id = 99999999999999999999999999999999
    min_time = datetime.now()
    for docs in database:
        data = database.get(docs)
        total_count += 1
        data_id = int(data['_id'])
        if data_id > max_id:
            max_id = data_id
        if data_id < min_id:
            min_id = data_id
        post_date_time = datetime.strptime(data["post_date_time"][0] + data["post_date_time"][1],
                                           '%Y-%m-%d%H:%M:%S')
        if post_date_time < min_time:
            min_time = post_date_time
    print("total count: ", total_count,
          "\nmax id is: ", max_id,
          "\nmin id is: ", min_id,
          "\nmin post date time is: ", min_time)
    return {"total_count": total_count,
            "max_id": max_id,
            "min_id": min_id,
            "min_time": min_time}


def wash_tweet(usr_id, raw_data):
    created = raw_data['created_at']
    created_time = datetime.strptime(created, '%a %b %d %H:%M:%S %z %Y')
    post_year = created_time.year
    post_month = created_time.month
    post_date = created_time.strftime('%Y-%m-%d')
    post_time = created_time.strftime('%H:%M:%S')
    new_data = {}
    new_data['_id'] = raw_data['id_str']
    new_data['usr_id'] = usr_id
    # new_data['tweet_id'] = status._json['id']
    new_data['post_date_time'] = [post_date, post_time]
    new_data['post_year'] = post_year
    new_data['post_month'] = post_month
    new_data['content'] = raw_data['full_text']
    new_data['hashtags'] = raw_data['entities']['hashtags']
    new_data['symbols'] = raw_data['entities']['symbols']
    new_data['user_mentions'] = raw_data['entities']['user_mentions']
    new_data['urls'] = raw_data['entities']['urls']
    new_data['favor_count'] = raw_data['favorite_count']
    new_data['retweet_count'] = raw_data['retweet_count']
    is_quote = raw_data['is_quote_status']
    new_data['is_quote_status'] = is_quote  # whether is a retweet
    return new_data

def update_usr_tweet(usr_id, db_name):
    database = couch[db_name]
    print("Gathering--", database, "--...")
    max_id = str(get_update_time(database)["max_id"])
    print("Updating--", database, "--...")
    t = 0
    count = 0
    docs = []
    for status in tweepy.Cursor(api.user_timeline, id=usr_id, max_id=max_id, tweet_mode='extended').items():
        # print(status._json)
        new_data = wash_tweet(usr_id, status._json)
        docs.append(new_data)
        t += 1
        count += 1
        print(database, "Updating data...", count)
        if t >= 1000:
            save_to_db(docs, database)
            docs = []
            t = 0
            print("Saving to db")

    save_to_db(docs, db_name)  # save the rest whose t is less than 1000



if __name__ == '__main__':
    school_id_name = [('86806243', 'msdsocial'), ('105996292', 'ArtsUnimelb'), ('1682489124', 'MSSIMelb'),
                      ('996929982738845697', 'williams_centre'), ('139893918', 'BusEcoNews'),
                      ('38076735', 'MelbBSchool'), ('1095167091261431808', 'UnimelbNOS'), ('1338343166', 'EduMelb'),
                      ('75678134', 'engunimelb'), ('2493752444', "cis_dc"), ('940445534556364800', "cis_unimelb"),
                      ('543070118', "vca_mcm"), ('3147075901', "alc_mls"), ('1338510631', "CCCSMelbourne"),
                      ('1032033930994638848', 'digcitzMLS'), ('778435773821358080', 'lprn_mls'),
                      ('911430326', 'MelbLawSchool'), ('1444962289', 'Government_UoM'), ('624336093', 'UnimelbMDHS'),
                      ('926261188991897601', 'UniMelbDOVS'), ('908546248231182336', 'UniMelbD4H'),
                      ('305326830', 'CHESM_unimelb'), ('873118533630152705', 'MMW_Initiative'),
                      ('309498998', 'UltrasoundEDU'), ('963976788513730560', 'UMCCR'),
                      ('868627442021277696', 'CritCareUnimelb'), ('2599851283', 'MRSP_Unimelb'),
                      ('1105685045308608512', 'SexHealthUoM'), ('1009623031700905984', 'HEU_unimelb'),
                      ('838602619828346880', 'HlthEquityMDHS'), ('114726495', 'CIMH'), ('3168090996', 'Psychunimelb'),
                      ('912515269406244864', 'UnimelbBME'), ('788803401819627520', 'StemCellsUoM'),
                      ('920798041803649024', 'MelbIntGen'), ('35929575', 'SciMelb'), ('1509295170', 'FVASunimelb'),
                      ('14862794', 'unimelb')]

    for id_name in school_id_name:
        sch_id = id_name[0]
        sch_name = id_name[1].lower()
        start_time = time.time()

        try:
            # update_usr_tweet(sch_id, sch_name)
            get_usr_information(sch_id, sch_name)

        except tweepy.TweepError:
            time_used = time.time() - start_time
            sleep_time = math.ceil(60 * 15 + 1 - time_used)
            time.sleep(sleep_time)
            print('Please be patient and wait...', sleep_time)


