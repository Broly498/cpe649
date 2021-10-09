#import matplotlib.pyplot as plt
import numpy as np
import gzip as gz
from numpysocket import NumpySocket
import socket as socket
import sys
from io import BytesIO

npSocket = NumpySocket()
npSocket.startServer(55555)
print("Image data server started")

compSocket = socket.socket()
compSocket.connect(('localhost', 55556))
print("Compression data client connected")

# Factor and clip used to increase visibility for plotting
factor=3.5/255
clip_range=(0, 1)

file_name = "runtime_image.dat"
compressed_file_name = "runtime_compressed.dat.gz"

while True:
    print("Waiting for image to be transmitted")
    uncompressed_image_data = npSocket.recieve()
    print("Image received: " + str(sys.getsizeof(uncompressed_image_data)))
    # Optional, show image when it is read
    #imgplot = plt.imshow(np.clip(uncompressed_image_data * factor, *clip_range))
    #plt.show()

    b = BytesIO()
    np.save(b, uncompressed_image_data, allow_pickle=True)
    binary_image_data = b.getvalue()
    compressed_image_data = gz.compress(binary_image_data)
    print("Sending compressed data: " + str(sys.getsizeof(compressed_image_data)))
    compressed_image_data += b'TRANSMISSION_STOP'
    compSocket.sendall(compressed_image_data)

npSocket.close()
compSocket.close()