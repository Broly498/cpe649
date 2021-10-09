import matplotlib.pyplot as plt
import numpy as np
import os
import time
import gzip as gz
from Crypto.Cipher import AES
import socket as socket
import sys
from io import BytesIO


# Factor and clip used to increase visibility for plotting
factor=3.5/255
clip_range=(0, 1)

file_name = "runtime_encrypted.bin"
key_file = "key_file.bin"
tag_file = "tag_file.bin"

while True:
    while not os.path.exists(file_name):
        time.sleep(1)

    if os.path.isfile(file_name):
        print("Encrypted data found. Unencrypting and decompressing...")
        time.sleep(5)
        #Get the encrypted data
        enfile = open(file_name, "rb")
        byteHolder = enfile.read()
        #Unencrypt the data
        #Get the tag
        tagfile = open(tag_file, "rb")
        tag2 = tagfile.read()
        #Get the key
        keyfile = open(key_file, "rb")
        key = keyfile.read()
        cipher = AES.new(key, AES.MODE_SIV)
        compressed_data = cipher.decrypt_and_verify(byteHolder, tag2)
        enfile.close()
        os.remove(file_name)
        print("Compressed data received: " + str(sys.getsizeof(compressed_data)))
        # Optional test, uncompress and display image
        uncompressed_data = BytesIO(gz.decompress(compressed_data))
        print("Data uncompressed: " + str(sys.getsizeof(uncompressed_data)))
        uncompressed_image_data = np.load(uncompressed_data, allow_pickle=True)
        imgplot = plt.imshow(np.clip(uncompressed_image_data * factor, *clip_range))
        plt.show()


