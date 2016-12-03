import os,sys,logging,time,shutil
from fabric.state import env
from fabric.api import env,local,run,sudo,put,cd,lcd,puts,task,get,hide
from settings import BUCKET_NAME,DATA_PATH,INDEX_PATH
try:
    import inception
except ImportError:
    print "could not import main module limited to boostrap actions"
    pass

from settings import USER,private_key,HOST
env.user = USER
env.key_filename = private_key
env.hosts = [HOST,]
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='logs/fab.log',
                    filemode='a')

@task
def server():
    """
    start server
    """
    local('python server.py')


@task
def demo_fashion():
    """
    Start Demo using precomputed index for 450 thousand female fashion images.
    """
    local('aws s3api get-object --bucket aub3visualsearch --key "fashion_index.tar.gz" --request-payer requester /mnt/fashion_index.tar.gz')
    local('cd /mnt/;tar -zxvf fashion_index.tar.gz')
    local('echo "\nDEMO=\'fashion_images\'" >> settings.py')
    local('echo "\nINDEX_PATH=\'/mnt/fashion_index/\'" >> settings.py')
    local('python server.py &')
    local('tail -f logs/server.log')


@task
def demo_nyc():
    """
    Start Demo using precomputed index for 26 thousand street view / dashcam style images.
    """
    local('aws s3api get-object --bucket aub3visualsearch --key "nyc_index.tar.gz" --request-payer requester /mnt/nyc_index.tar.gz')
    local('cd /mnt/;tar -zxvf nyc_index.tar.gz')
    local('echo "\nDEMO=\'nyc_images\'" >> settings.py')
    local('echo "\nINDEX_PATH=\'/mnt/nyc_index/\'" >> settings.py')
    local('python server.py &')
    local('tail -f logs/server.log')


@task
def index():
    """
    Index images
    """
    logging.info("Starting with images present in {} storing index in {}".format(DATA_PATH,INDEX_PATH))
    try:
        os.mkdir(INDEX_PATH)
    except:
        print "Could not created {}, if its on /mnt/ have you set correct permissions?".format(INDEX_PATH)
        raise ValueError
    inception.load_network()
    count = 0
    start = time.time()
    with inception.tf.Session() as sess:
        for image_data in inception.get_batch(DATA_PATH):
            logging.info("Batch with {} images loaded in {} seconds".format(len(image_data),time.time()-start))
            start = time.time()
            count += 1
            features,files = inception.extract_features(image_data,sess)
            logging.info("Batch with {} images processed in {} seconds".format(len(features),time.time()-start))
            start = time.time()
            inception.store_index(features,files,count,INDEX_PATH)

@task
def clear():
    """
    delete logs
    """
    local('rm logs/*.log &')


@task
def test():
    inception.load_network()
    count = 0
    start = time.time()
    test_images =  os.path.join(os.path.dirname(__file__),'tests/images')
    test_index = os.path.join(os.path.dirname(__file__), 'tests/index')
    try:
        shutil.rmtree(test_index)
    except:
        pass
    os.mkdir(test_index)
    with inception.tf.Session() as sess:
        for image_data in inception.get_batch(test_images,batch_size=2):
            # batch size is set to 2 to distinguish between latency associated with first batch
            if len(image_data):
                print "Batch with {} images loaded in {} seconds".format(len(image_data),time.time()-start)
                start = time.time()
                count += 1
                features,files = inception.extract_features(image_data,sess)
                print "Batch with {} images processed in {} seconds".format(len(features),time.time()-start)
                start = time.time()
                inception.store_index(features,files,count,test_index)
