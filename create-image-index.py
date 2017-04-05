
import tensorflow, inception
from inception import *
import urllib
import psycopg2
#import cv2

inception.load_network()
count = 0
start = time.time()

try:
    conn = psycopg2.connect("dbname='YOUR_DB_NAME' user='YOUR_USER' host='YOUR_HOST' password='YOUR_PASSWORD'")
except:
    print "Unable to connect to the database"

cur = conn.cursor()

try:
    cur.execute("""select category,data->'imUrl' from datasets where category='belts'""")
except:
    print "Error fetching belts entries from database."

rows = cur.fetchall()


with inception.tf.Session() as sess:
    pool3 = sess.graph.get_tensor_by_name('incept/pool_3:0')
    features = []
    files = []
    
    for row in rows:
        imgUrl = row[1]
        print imgUrl

        if ".jpg" in imgUrl:
            try:
                image = urllib.urlopen(imgUrl)
                pool3_features = sess.run(pool3,{'incept/DecodeJpeg/contents:0': image.read()})
                features.append(np.squeeze(pool3_features))
                files.append(imgUrl)
            except Exception as e:
                print e
    inception.store_index(features,files,len(rows),INDEX_PATH)
