import couchdb
server = couchdb.Server('http://ailinz1:unimelb666@10.13.23.153:5984')
# db=server['raw_tweets']
db = server['_replicator']
try:
    db2=server.create('result')
except:
    db2=server['result']

print(db['_design/_replicator'].keys())

db2.save(dict({"NumTweets19":1}))

data = db2["Unimelb"]
data['billSeconds'] = 191
db2.save(data)

