Visual Search Server [![](https://images.microbadger.com/badges/image/akshayubhat/visualsearchserver.svg)](https://microbadger.com/images/akshayubhat/visualsearchserver "Get your own image badge on microbadger.com")
===============

**The in this repo works however as of Jan 2017 I am now working on Deep Video Analytics which provides a more complete set of functionality for video and image analytics in addition to all the features provided by this repository. You can find the [Deep Video Analytics repo here](https://github.com/akshayubhat/DeepVideoAnalytics).**

A simple implementation of Visual Search using TensorFlow, InceptionV3 model and AWS GPU instances.
This codebase implements a simple visual indexing and search system, using features derived from Google's inception 
model trained on the imagenet data. The easist way to use it is to launch following AMI using GPU enabled g2 instances.
It already contains features computed on ~450,000 images (female fashion), the feature computation took 22 hours on 
a spot AWS g2 (single GPU) instance. i.e. ~ 230,000 images / 1 $ . Since I did not use batching, it might be possible to 
get even better performance.

The code implements two methods, a server that handles image search, and a simple indexer that extracts pool3 features.
Nearest neighbor search can be performed in an approximate manner using nearpy (faster) or using exact methods (slower).
 
![UI Screenshot](appcode/static/alpha3.png "Alpha Screenshot Female Fashion")
![UI Screenshot](appcode/static/alpha4.png "Alpha Screenshot NYC, Streetview & Dashcam")

####Running code using docker and nvidia-docker

Visual Search Server GPU image created using nvidia-docker is [available on dockerhub](https://hub.docker.com/r/akshayubhat/visualsearchserver/).
```
docker pull akshayubhat/visualsearchserver
```

This repo now contains a dockerfile in the /docker folder for both gpu and cpu use.
To build the docker image edit the fabfile in docker folder by specifying name for the image and run.
``` 
fab buid # to build the docker image (you can then edit and push to your docker registry)
fab start # to start jupyter notebook 
fab server # to start retrieval server
fab rm # to stop and remove all data associated with the image
```

####Index images
The code provides a single index operation to index images using Pool3 features.
Store all images in a single directory, specify path to that directory. 
Specify path to a directory for storing indexes.   
```
# edit settings.py
INDEX_PATH = "/mnt/nyc_index/" 
DATA_PATH ="/mnt/nyc_images/" # /mnt/ is mounted with instance store on AWS
```
To perform indexing run following. 
```
  cd ~/VisualSearchServer/
  fab index &
  tail -f logs/worker.log
```

####Run demo with precomputed index  
Note that following code will download about ~3Gb indexes from S3 and it will also download individual images while generating results for queries.
This should not be a problem when running on AWS / correct region. It will take about 2 minutes (NYC) ~ 10 minutes (Fashion)  to download, extract and load index in the memory.
```
cd VisualSearchServer
git pull
sudo chmod 777 /mnt/
fab demo_fashion
// or run dashcam/streetview/nyc demo
fab demo_nyc
```
A successful completion will result in following message:
```
03-09 11:33 werkzeug     INFO      * Running on http://0.0.0.0:9000/ (Press CTRL+C to quit)
```
You can then  use browser to access web UI on port 9000 of the instance DNS/IP.

#### Following libraries & templates are used:
1. https://almsaeedstudio.com/
2. http://fabricjs.com/kitchensink
3. https://github.com/karpathy/convnetjs
4. https://www.tensorflow.org/ 
5. http://pixelogik.github.io/NearPy/

   
License:    
I plan to switch to an Apache 2.0 license soon, staty tuned. Please contact me if you have any questions in the meantime. 
