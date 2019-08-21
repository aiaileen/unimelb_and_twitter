import couchdb
import re
from _datetime import datetime

# local_host = "http://ailinz1:unimelb666@localhost:5984"
# local_couch = couchdb.Server(local_host)
# remote_host = "http://admin:admin@45.113.233.247:5984"
# remote_couch = couchdb.Server(remote_host)


def getDB(database):
    db_host = "http://admin:admin@45.113.233.247:5984"
    couch = couchdb.Server(db_host)
    db = couch[database]
    return db

def save_to_newdb(data, db_name):
    db_host = "http://admin:admin@45.113.233.247:5984"
    couch = couchdb.Server(db_host)
    try:
        db = couch[db_name]
        newdata_id = data['_id']
        for ids in db:
            if ids is newdata_id:
                return False  # if already exsits, save failed
    except:
        db = couch.create(db_name)
    db.save(data)
    return True


def filter_retweet(sch_name):
    db = getDB(sch_name)
    t = 0
    for ids in db:
        doc = db[ids]
        tweet = doc['content']
        begin_letter = tweet[0:2]
        tmp = re.split(r'https://', tweet)
        tweet_text = tmp[0]

        if begin_letter == 'RT':
            print("===skipping===")
            continue
        else:
            t += 1
            print("Updating", t)
            new_doc = {}
            new_doc['_id'] = doc['_id']
            new_doc["usr_id"] = doc["usr_id"]
            new_doc["post_date_time"] = doc["post_date_time"]
            new_doc["post_year"] = doc["post_year"]
            new_doc["post_month"] = doc["post_month"]
            new_doc["content"] = tweet_text
            new_doc["favor_count"] = doc["favor_count"]
            new_doc["retweet_count"] = doc["retweet_count"]

            result = save_to_newdb(new_doc, sch_name)
            # if result:
            #     print("Successfully saved~")
            # else:
            #     print("Oops..This data already exists...")
            # print (tweet)


def gather_result(sch_name):
    db_host = "http://admin:admin@45.113.233.247:5984"
    couch = couchdb.Server(db_host)
    db = couch[sch_name]
    try:
        resultdb = couch.create('result')
    except:
        resultdb = couch['result']

    NumTweets19 = 0
    NumTweets18 = 0
    NumTweets17 = 0
    NumTweets16 = 0
    NumTweets15 = 0
    NumLikes = 0
    NumRetwe = 0

    for key in db:
        doc = db.get(key)
        date = doc['post_year']
        if date == 2019:
            NumTweets19 += 1
        elif date == 2018:
            NumTweets18 += 1
        elif date == 2017:
            NumTweets17 += 1
        elif date == 2016:
            NumTweets16 += 1
        elif date == 2015:
            NumTweets15 += 1

        if doc['favor_count'] != 0:
            NumLikes += 1
        # AvgLikes= NumLikes/(NumTweets19 + NumTweets18 + NumTweets17 + NumTweets16 + NumTweets15)

        if doc['retweet_count'] != 0:
            NumRetwe += 1

    try:
        doc = resultdb.get(sch_name)
        doc["NumTweets19"] = NumTweets19
        doc["NumTweets18"] = NumTweets18
        doc["NumTweets17"] = NumTweets17
        doc["NumTweets16"] = NumTweets16
        doc["NumTweets15"] = NumTweets15
        doc["NumLikes"] = NumLikes
        doc["NumRetwe"] = NumRetwe
    except:
        doc = {}
        doc['_id'] = sch_name
        doc["NumTweets19"] = NumTweets19
        doc["NumTweets18"] = NumTweets18
        doc["NumTweets17"] = NumTweets17
        doc["NumTweets16"] = NumTweets16
        doc["NumTweets15"] = NumTweets15
        doc["NumLikes"] = NumLikes
        doc["NumRetwe"] = NumRetwe
        resultdb.save(doc)


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
        sch_name = id_name[1].lower()
        print("Processing..", sch_name)

        filter_retweet(sch_name)
        gather_result(sch_name)






