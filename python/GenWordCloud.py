from PIL import Image
import numpy as np
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

import couchdb
db_host = "http://admin:admin@45.113.233.247:5984"
couch = couchdb.Server(db_host)


def get_tweet_txt(school):
    for sch in school:
        file_name = sch[0]+'.txt'
        f = open(file_name, 'a')
        print("processing", file_name)
        for names in sch[1]:
            sch_name = names.lower()
            db = couch[sch_name]
            for doc_name in db:
                data = db.get(doc_name)
                tweet = data['content']
                f.write(' '+tweet)
        # f.closed()
    print('all done')


def generate_word_cloud(school):
    cloud_mask = np.array(Image.open('cloudmask.png'))
    for sch in school:
        file_name = sch[0]+'.txt'
        txt = open(file_name, 'r').read()
        stopwords = set('')
        old = set(STOPWORDS)
        stopwords.update(['bitly','RT', 'co', 'bit', 'ow', 'ly', 'owly',
                          'amp', 'MB', 'goo', 'gl', 'googl', 'unimelb',
                          'will', 'new','student','Australia', 'students'])
        new_stopwords = old.union(stopwords)

        word_cloud = WordCloud(background_color='white',
                               # max_words=2000,
                               mask=cloud_mask,
                               stopwords=new_stopwords,
                               # width=2000, height=860,
                                scale=3)
        word_cloud.generate(txt)

        # image_colors = ImageColorGenerator(cloud_mask)
        plt.imshow(word_cloud, interpolation='bilinear')
        plt.axis("off")
        plt.figure()
        plt.imshow(cloud_mask, cmap=plt.cm.gray, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        word_cloud.to_file( sch[0] + ".jpg")


if __name__ == '__main__':
    abp = ['msdsocial']
    arts =['ArtsUnimelb', 'MSSIMelb']
    be = ['williams_centre', 'BusEcoNews', 'MelbBSchool']
    education = ['UnimelbNOS', 'EduMelb']
    engineering = ['engunimelb', 'cis_dc', 'cis_unimelb']
    fam = ['vca_mcm']
    law = ['alc_mls', 'CCCSMelbourne', 'digcitzMLS',
           'lprn_mls', 'MelbLawSchool', 'Government_UoM']
    mdhs = ['UnimelbMDHS', 'UniMelbDOVS', 'UniMelbD4H', 'CHESM_unimelb',
            'MMW_Initiative', 'UltrasoundEDU', 'UMCCR', 'CritCareUniMelb',
            'MRSP_Unimelb', 'SexHealthUoM', 'HEU_unimelb', 'HlthEquityMDHS',
            'CIMH', 'Psychunimelb', 'UnimelbBME', 'StemCellsUoM']
    science = ['MelbIntGen', 'SciMelb']
    vas = ['FVASunimelb']
    homepage = ['unimelb']

    schools = [('abp', abp), ('arts', arts), ('be', be), ('education', education),
               ('engineering', engineering), ('fam', fam), ('law', law), ('mdhs', mdhs),
               ('science', science), ('vas', vas), ('homepage', homepage)
               ]

    get_tweet_txt(schools)
    generate_word_cloud(schools)