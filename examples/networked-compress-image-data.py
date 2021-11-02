import numpy as np
import gzip as gz
from numpysocket import NumpySocket
import socket as socket
import sys
import time
from io import BytesIO

clientIpAddress = 'localhost'
clientPort = 55556
serverPort = 55555

isConnected = False
retryAttempt = 0
maximumNumberOfRetries = 10
i = 1

if len(sys.argv) > 1:
    clientIpAddress = sys.argv[1]

npSocket = NumpySocket()
print("Starting time compression: " + str(time.time_ns()), flush=True)
print("Starting image data server on port " + str(serverPort) + ".", flush=True)
npSocket.startServer(serverPort)
print("Image data server started", flush=True)
compSocket = socket.socket()
print("Attempting to connect to " + clientIpAddress + ":" + str(clientPort) + ".", flush=True)

while not isConnected:
    try:
        compSocket.connect((clientIpAddress, clientPort))
        isConnected = True
    except Exception:
        if retryAttempt >= maximumNumberOfRetries:
            print("Failed to connect, maximum number of retries exceeded.", flush=True)
            quit()
        else:
            retryAttempt += 1
            print("Failed to connect, retrying in 5 seconds. Retry attempt " + str(retryAttempt) + " out of " + str(maximumNumberOfRetries) + ".", flush=True)
            time.sleep(5)

print("Compression data client connected", flush=True)

file_name = "runtime_image.dat"
compressed_file_name = "runtime_compressed.dat.gz"

while i <= 25:
    print("Waiting for image to be transmitted", flush=True)
    uncompressed_image_data = npSocket.recieve()
    print("Image received: " + str(sys.getsizeof(uncompressed_image_data)), flush=True)
    print("Time image received: " + str(time.time_ns()), flush=True)

    b = BytesIO()
    np.save(b, uncompressed_image_data, allow_pickle=True)
    binary_image_data = b.getvalue()
    compressed_image_data = gz.compress(binary_image_data)
    print("Sending compressed data: " + str(sys.getsizeof(compressed_image_data)), flush=True)
    compressed_image_data += b'TRANSMISSION_STOP'
    compSocket.sendall(compressed_image_data)
    i = i + 1

npSocket.close()
compSocket.close()
