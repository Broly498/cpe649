# # Sentinel Hub's Sentinel-2 Cloud Detector
# 
# This example notebook shows how to perform cloud classification and cloud masking on Sentinel-2 data.
# 
# In the process we will use [`sentinelhub-py`](https://github.com/sentinel-hub/sentinelhub-py) Python package. The package documentation is available [here](https://sentinelhub-py.readthedocs.io/en/latest/).
# 
# ## Prerequisite
# 
# ### Imports

#import matplotlib.pyplot as plt
import numpy as np

import time

#from sentinelhub import SHConfig, BBox, CRS, SentinelHubRequest, DataCollection, \
#    MimeType, bbox_to_dimensions

from s2cloudless import S2PixelCloudDetector

from numpysocket import NumpySocket

#s = socket.socket()
#s.bind(('localhost', 55555))
#s.listen(1)
#print("Waiting to connect to client...")
#conn, addr = s.accept()
#print("Connected to: " + str(addr[0]))

npSocket = NumpySocket()
npSocket.startClient('localhost', 55555)
print("Image data client connected")

# Factor and clip used to increase visibility for plotting
factor=3.5/255
clip_range=(0, 1)

result_file_name = "runtime_image.dat"

#TODO Up range to 26 for full run
for i in range(1,26):
    print("Processing image: " + str(i))
    image_file_name = "image_" + str(i) + ".dat"
    data_file_name = "data_" + str(i) + ".dat"

    image_file = open(image_file_name, "rb")
    image_data = np.load(image_file)
    image_file.close()

    print("Candidate image: " + str(i))

    data_file = open(data_file_name, "rb")
    full_data = np.load(data_file)
    data_file.close()

    #mask = full_data[..., -1]

    # ### Initialize the cloud detector and make classification
    # 
    # We can specify the following arguments in the initialization of a `S2PixelCloudDetector`:
    # 
    #  * `threshold` - cloud probability threshold value. All pixels with cloud probability above threshold value are masked as cloudy pixels. Default is `0.4`.
    #  * `average_over` - Size of the disk in pixels for performing convolution (averaging probability over pixels). For this resolution `4` is appropriate. 
    #  * `dilation_size` - Size of the disk in pixels for performing dilation.  For this resolution `2` is appropriate.
    #  * `all_bands` - Flag specifying that input images will consists of all 13 Sentinel-2 bands. It has to be set to `True` if we would download all bands. If you define a layer that would return only 10 bands, then this parameter should be set to `False`.

    cloud_detector = S2PixelCloudDetector(
        threshold=0.6,
        average_over=4,
        dilation_size=2,
        all_bands=False,
        model_filename = 'cloud_detector_model.txt'
    )

    # #### Run the classification
    # 
    # There are two possibilities:
    #  * `get_cloud_probability_maps` will return cloud probability map
    #  * `get_cloud_masks` will return binary cloud masks
    
    #print("\nComputing cloud probabilities")
    #start_time = time.time()
    #cloud_prob = cloud_detector.get_cloud_probability_maps(full_data)
    #print("Cloud probabilities computed. Time: %s" % (time.time() - start_time))

    print("\nComputing cloud masks")
    start_time = time.time()
    cloud_mask = cloud_detector.get_cloud_masks(full_data)
    print("Cloud masks computed. Time: %s" % (time.time() - start_time))

    cloud_pixels = np.count_nonzero(cloud_mask)
    total_pixels = np.size(cloud_mask)
    print("Computed cloud pixels/total pixels: " + str(cloud_pixels) + "/" + str(total_pixels))
    cloud_ratio = float(cloud_pixels)/float(total_pixels)
    print("Cloud ratio: " + str(cloud_ratio))

    # Optional, print cloud recognition results
    '''
    plt1 = plt.subplot(1, 2, 1)
    plt1.imshow(np.clip(image_data * factor, *clip_range))
    plt2 = plt.subplot(1, 2, 2)
    plt2.imshow(np.clip(image_data * factor, *clip_range))
    cloud_image = np.zeros((cloud_mask.shape[0], cloud_mask.shape[1], 4), dtype=np.uint8)
    cloud_image[cloud_mask == 1] = np.asarray([255, 255, 0, 100], dtype=np.uint8)
    plt2.imshow(cloud_image)
    plt.show()
    '''

    if cloud_ratio < 50.0:
        print("Image accepted, transmitting...")
        npSocket.send(image_data)
        
    else:
        print("Image rejected")

npSocket.close()