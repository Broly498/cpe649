import matplotlib.pyplot as plt
import numpy as np
from sentinelhub import SHConfig, BBox, CRS, SentinelHubRequest, DataCollection, \
    MimeType, bbox_to_dimensions
from s2cloudless import get_s2_evalscript
#from plotting_utils import plot_image
import random

CLIENT_ID = "e219d2c4-75d0-4d89-9c1d-85f6ece41395"
CLIENT_SECRET = "?Zkj<NHNxZKDqbvKtTReOaA|:**.xt7N96puO;pa"
config = SHConfig()
if CLIENT_ID and CLIENT_SECRET:
    config.sh_client_id = CLIENT_ID
    config.sh_client_secret = CLIENT_SECRET

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

# Factor and clip used to increase visibility for plotting
factor=3.5/255
clip_range=(0, 1)

# Values used to generate regions of approximately 7x7 km
longitude_offset = 0.082
lattitude_offset = 0.062

#test_file = open("hsv_color.dat", "rb")
#true_color_test = np.load(test_file)
#imgplot = plt.imshow(np.clip(true_color_test * factor, *clip_range))
#plt.show()

i = 1
while True:
    print("Generating new guess")
    # Note: Guesses are roughly bounded to the US to avoid a bunch of ocean images
    random_longitude = random.uniform(-75.0, -125.0)
    random_lattitude = random.uniform(25.0, 50.0)
    #bbox = BBox([-86.6953, 34.6892, -86.5923, 34.7613], crs=CRS.WGS84)
    bbox = BBox([random_longitude, random_lattitude, random_longitude + longitude_offset, random_lattitude + lattitude_offset], crs=CRS.WGS84)
    request = SentinelHubRequest(
        evalscript=evalscript_true_color,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L1C,
                time_interval='2021-09-01'
            )
        ],
        responses=[
            SentinelHubRequest.output_response('default', MimeType.PNG)
        ],
        bbox=bbox,
        size=bbox_to_dimensions(bbox, 10),
        config=config
    )
    candidate_image = request.get_data()[0]
    if not np.any(candidate_image):
        print("No data available guessed date/location")
        continue
    imgplot = plt.imshow(np.clip(candidate_image * factor, *clip_range))
    plt.show()
    image_good = input("Is this image good (y/n): ")
    if image_good == 'y':
        image_file_name = "image_" + str(i) + ".dat"
        data_file_name = "data_" + str(i) + ".dat"
        print("Storing true color data in: " + image_file_name)
        file_color = open(image_file_name, "wb")
        np.save(file_color, candidate_image)
        file_color.close

        evalscript = get_s2_evalscript(all_bands=False, reflectance=True)
        request = SentinelHubRequest(
            evalscript=evalscript,
            input_data=[
                SentinelHubRequest.input_data(
                    data_collection=DataCollection.SENTINEL2_L1C,
                    time_interval='2021-09-01'
                )
            ],
            responses=[
                SentinelHubRequest.output_response('default', MimeType.TIFF)
            ],
            bbox=bbox,
            size=bbox_to_dimensions(bbox, 10),
            config=config
        )
        candidate_data = request.get_data()[0]
        candidate_data = candidate_data[..., :-1]
        print("Storing full data in: " + data_file_name)
        file_data = open(data_file_name, "wb")
        np.save(file_data, candidate_data)
        file_data.close

        i += 1

    elif image_good == 'n':
        continue

    else:
        break
