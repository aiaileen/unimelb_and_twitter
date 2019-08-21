import couchdb
server = couchdb.Server('http://admin:admin@45.113.233.247:5984')
#每个账户有一个数据库，存储了所有这个账户发的tweets。
#统计之后的结果放在一个叫result的数据库里，存储在名称与这个账户相同的doc里。
servers = ['msdsocial', 'ArtsUnimelb', 'MSSIMelb', 'williams_centre', 
'BusEcoNews', 'MelbBSchool', 'UnimelbNOS', 'EduMelb', 
'engunimelb', 'cis_dc', 'cis_unimelb', 'vca_mcm', 
'alc_mls', 'CCCSMelbourne', 'digcitzMLS', 'lprn_mls', 
'MelbLawSchool', 'Government_UoM', 'UnimelbMDHS', 'UniMelbDOVS', 
'UniMelbD4H', 'CHESM_unimelb', 'MMW_Initiative', 'UltrasoundEDU', 
'UMCCR', 'CritCareUnimelb', 'MRSP_Unimelb', 'SexHealthUoM', 
'HEU_unimelb', 'HlthEquityMDHS', 'CIMH', 'Psychunimelb', 
'UnimelbBME', 'StemCellsUoM', 'MelbIntGen', 'SciMelb', 
'FVASunimelb', 'unimelb']

try:
    db2=server.create('result')
except:
    db2=server['result']

for db in servers:
    dblower = db.lower()
    db1=server[dblower]
    NumTweets19 = 0
    NumTweets18 = 0
    NumTweets17 = 0
    NumTweets16 = 0
    NumTweets15 = 0
    NumLikes = 0
    NumRetwe = 0

    for key in db1:
        doc = db1.get(key)
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

    print(dblower)

    try:
        doc = db2.get(dblower)
        doc["NumTweets19"] = NumTweets19
        doc["NumTweets18"] = NumTweets18
        doc["NumTweets17"] = NumTweets17
        doc["NumTweets16"] = NumTweets16
        doc["NumTweets15"] = NumTweets15
        doc["NumLikes"] = NumLikes
        doc["NumRetwe"] = NumRetwe
    except:
        doc = {}
        doc['_id'] = dblower
        doc["NumTweets19"] = NumTweets19
        doc["NumTweets18"] = NumTweets18
        doc["NumTweets17"] = NumTweets17
        doc["NumTweets16"] = NumTweets16
        doc["NumTweets15"] = NumTweets15
        doc["NumLikes"] = NumLikes
        doc["NumRetwe"] = NumRetwe
        db2.save(doc)

    db2.save(doc)
