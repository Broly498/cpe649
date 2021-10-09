import matplotlib.pyplot as plt
import os
import time
import numpy as np
import gzip as gz

# Factor and clip used to increase visibility for plotting
factor=3.5/255
clip_range=(0, 1)

file_name = "runtime_image.dat"
compressed_file_name = "runtime_compressed.dat.gz"

while True:
    print("Waiting for " + file_name + " to be created. Ctrl-C to terminate")

    while not os.path.exists(file_name):
        time.sleep(1)

    if os.path.isfile(file_name):
        print("Image data found. Compressing...")
        uncompressed_file = open(file_name, "rb")
        uncompressed_image_data = np.load(uncompressed_file)
        uncompressed_file.close()
        os.remove(file_name)
        # Optional, show image when it is read
        imgplot = plt.imshow(np.clip(uncompressed_image_data * factor, *clip_range))
        plt.show()
        # Create compressed file
        compressed_file = gz.GzipFile(compressed_file_name, "wb")
        np.save(compressed_file, uncompressed_image_data)
        compressed_file.close()

    # Test that data is still good when opened
    #print("Printing data read from: " + compressed_file_name)
    #f = gz.GzipFile(compressed_file_name, "r")
    #test_compressed_data = np.load(f)
    #imgplot = plt.imshow(np.clip(test_compressed_data * factor, *clip_range))
    #plt.show()
