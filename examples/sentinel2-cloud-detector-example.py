#!/usr/bin/env python
# coding: utf-8

# # Sentinel Hub's Sentinel-2 Cloud Detector
# 
# This example notebook shows how to perform cloud classification and cloud masking on Sentinel-2 data.
# 
# In the process we will use [`sentinelhub-py`](https://github.com/sentinel-hub/sentinelhub-py) Python package. The package documentation is available [here](https://sentinelhub-py.readthedocs.io/en/latest/).
# 
# ## Prerequisite
# 
# ### Imports

import sys
import datetime as dt

import matplotlib.pyplot as plt
import numpy as np

import time

from sentinelhub import SHConfig, BBox, CRS, SentinelHubRequest, DataCollection, \
    MimeType, bbox_to_dimensions

from s2cloudless import S2PixelCloudDetector, CloudMaskRequest, get_s2_evalscript

from plotting_utils import plot_image, plot_probabilities



# ### Sentinel Hub credentials
# 
# These examples require Sentinel Hub OAuth client credentials. Please check [`sentinelhub-py` configuration instructions](https://sentinelhub-py.readthedocs.io/en/latest/configure.html#sentinel-hub-capabilities) on how to obtain the credentials and configure them in the package.


# In case you put the credentials into the configuration file you can leave this unchanged
CLIENT_ID = "86ad3cec-1e7e-4b43-8145-1684ac658740"
CLIENT_SECRET = "ny9tEbtGx075%;Bm~3E5M_gYAFiu/j0)vQc4.4E_"

config = SHConfig()

if CLIENT_ID and CLIENT_SECRET:
    config.sh_client_id = CLIENT_ID
    config.sh_client_secret = CLIENT_SECRET

# ## Download and calculate cloud masks
# 
# In the first example we will separate the process in `2` parts:
# 
# 1. download satellite data
# 2. calculate cloud masks and probabilities from data
# 
# This will show how to perform cloud detection independetly from obtaining data.
# 
# 
# ### Example scenes: Acatenango and Volcan Fuego (Guatemala) in December 2017
# 
# Acatenango area in Guatemala is well known for its coffee plantations. At the altitute of about 2000 m and given it’s climate, it is often veiled in clouds.
# 
# First, lets define the bounding box for the area of interest:

if len(sys.argv) == 5:
    print("Using custom coordinates: %s" % sys.argv[1:])
    bbox = BBox([float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])], crs=CRS.WGS84)
else:
    print("Using default coordinates")
    bbox = BBox([-90.9217, 14.4191, -90.8187, 14.5520], crs=CRS.WGS84)

print(bbox)

#sys.exit()
# ### Download Sentinel-2 data
# 
# Let's download data using [Sentinel Hub Process API](https://docs.sentinel-hub.com/api/latest/api/process/). First let's download a true color image for which we want detect clouds. The downloaded image will be on a resolution `10` meter per pixel.

evalscript_true_color = """
    //VERSION=3

    function setup() {
        return {
            input: [{
                bands: ["B02", "B03", "B04"]
            }],
            output: {
                bands: 3
            }
        };
    }

    function evaluatePixel(sample) {
        return [sample.B04, sample.B03, sample.B02];
    }
"""

request = SentinelHubRequest(
    evalscript=evalscript_true_color,
    input_data=[
        SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL2_L1C,
            time_interval='2017-12-01'
        )
    ],
    responses=[
        SentinelHubRequest.output_response('default', MimeType.PNG)
    ],
    bbox=bbox,
    size=bbox_to_dimensions(bbox, 10),
    config=config
)

print("\nRequesting true color data")
start_time = time.time()

true_color_image = request.get_data()[0]

print("True color data received. Time: %s" % (time.time() - start_time))

true_color_image.shape

plt.plot([1,2,3])
plt.show

plot_image(true_color_image)
plt.show
plt.imshow(true_color_image)
plt.show

# Next, let's download remaining Sentinel-2 bands. `s2cloudless` detector only requires `10` out of `13` bands for cloud detection. The following utility will create an evalscript for requesting those bands.
# 
# For simplicity we will request data with reflectance values. To decrease download costs a better option is to download data in digital numbers (i.e. unsigned ints) and then rescale them with normalization factors. That is implemented in `CloudMaskRequest` class which will be shown below.

evalscript = get_s2_evalscript(
    all_bands=False,
    reflectance=True
)

# print(evalscript)

request = SentinelHubRequest(
    evalscript=evalscript,
    input_data=[
        SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL2_L1C,
            time_interval='2017-12-01'
        )
    ],
    responses=[
        SentinelHubRequest.output_response('default', MimeType.TIFF)
    ],
    bbox=bbox,
    size=bbox_to_dimensions(bbox, 10),
    config=config
)

print("\nRequesting multi-band data")
start_time = time.time()

data = request.get_data()[0]

print("Multi-band data received. Time: %s" % (time.time() - start_time))

bands = data[..., :-1]
mask = data[..., -1]

bands.shape, mask.shape

# ### Initialize the cloud detector and make classification
# 
# We can specify the following arguments in the initialization of a `S2PixelCloudDetector`:
# 
#  * `threshold` - cloud probability threshold value. All pixels with cloud probability above threshold value are masked as cloudy pixels. Default is `0.4`.
#  * `average_over` - Size of the disk in pixels for performing convolution (averaging probability over pixels). For this resolution `4` is appropriate. 
#  * `dilation_size` - Size of the disk in pixels for performing dilation.  For this resolution `2` is appropriate.
#  * `all_bands` - Flag specifying that input images will consists of all 13 Sentinel-2 bands. It has to be set to `True` if we would download all bands. If you define a layer that would return only 10 bands, then this parameter should be set to `False`.

cloud_detector = S2PixelCloudDetector(
    threshold=0.4,
    average_over=4,
    dilation_size=2,
    all_bands=False
)

# #### Run the classification
# 
# There are two possibilities:
#  * `get_cloud_probability_maps` will return cloud probability map
#  * `get_cloud_masks` will return binary cloud masks

print("\nComputing cloud probabilities")
start_time = time.time()

cloud_prob = cloud_detector.get_cloud_probability_maps(bands)

print("Cloud probabilities computed. Time: %s" % (time.time() - start_time))

print("\nComputing cloud masks")
start_time = time.time()

cloud_mask = cloud_detector.get_cloud_masks(bands)

print("Cloud masks computed. Time: %s" % (time.time() - start_time))

# ### Visualize the results
# 
# We have a binary cloud mask:

plot_image(mask=cloud_mask)
plt.show

# Let's plot a true color image overlaid with the cloud mask:

plot_image(image=true_color_image, mask=cloud_mask)
plt.show

# Besides that we also have pseudo-probability scores telling us how likely it is that certain pixel is cloudy:

plot_probabilities(true_color_image, cloud_prob)

# ## Use `CloudMaskRequest` to produce cloud masks

# `CloudMaskRequest` class combines download procedure with cloud detection. It works in a way that it processes all images from a given time interval and not just a single one. The process is optimized for performance and download costs.
# 
# The main input of `CloudMaskRequest`in an instance of cloud detector object. Additionally, we have to specify parameters defining location, time interval, etc. This time we'll download all Sentinel-2 bands only to have all RBG bands for visualization.

'''
cloud_detector = S2PixelCloudDetector(
    threshold=0.4,
    average_over=1,
    dilation_size=1,
    all_bands=True
)

cloud_mask_request = CloudMaskRequest(
    cloud_detector,
    bbox=bbox,
    time=('2017-12-01', '2017-12-31'),
    size=bbox_to_dimensions(bbox, 60),
    time_difference=dt.timedelta(hours=2),
    config=config
)

# So far no data has been downloaded or processed. The class only made a request to [Sentinel Hub Catalog API](https://docs.sentinel-hub.com/api/latest/api/catalog/) to obtain information when data is available. Those are the following timestamps:

cloud_mask_request.get_timestamps()

# The following will trigger download and cloud masking process:

cloud_masks = cloud_mask_request.get_cloud_masks()

cloud_masks.shape

# Let's extract RGB bands:

true_color_images = cloud_mask_request.get_data()[..., [3, 2, 1]]

true_color_images.shape

# Let's plot cloud masks together with images:

fig = plt.figure(figsize=(15, 10))
n_cols = 4
n_rows = int(np.ceil(len(true_color_images) / n_cols))

for idx, (image, mask) in enumerate(zip(true_color_images, cloud_masks)):
    ax = fig.add_subplot(n_rows, n_cols, idx + 1)
    plot_image(image, mask, ax=ax, factor=3.5)
    
plt.tight_layout()

# If the default probability threshold of `0.4` doesn't suit us we can override it to compute new binary cloud masks with a different threshold:

cloud_masks_different_threshold = cloud_mask_request.get_cloud_masks(threshold=0.2)

fig = plt.figure(figsize=(15, 10))
n_cols = 4
n_rows = int(np.ceil(len(true_color_images) / n_cols))

for idx, (image, mask) in enumerate(zip(true_color_images, cloud_masks_different_threshold)):
    ax = fig.add_subplot(n_rows, n_cols, idx + 1)
    plot_image(image, mask, ax=ax, factor=3.5)
    
plt.tight_layout()
'''
