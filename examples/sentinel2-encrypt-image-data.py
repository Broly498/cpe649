import matplotlib.pyplot as plt
import os
import time
import gzip as gz
from Crypto.Cipher import AES

# Factor and clip used to increase visibility for plotting
factor=3.5/255
clip_range=(0, 1)

file_name = "runtime_compressed.dat.gz"
encrypted_file_name = "runtime_encrypted.bin"
key_file = "key_file.bin"
tag_file = "tag_file.bin"

while True:
    print("Waiting for " + file_name + " to be created. Ctrl-C to terminate")

    while not os.path.exists(file_name):
        time.sleep(1)

    if os.path.isfile(file_name):
        print("Image data found. Compressing...")
        compressed_file = gz.GzipFile(file_name, "rb")
        data = compressed_file.read()
        compressed_file.close()
        os.remove(file_name)
        # Optional, show image when it is read
        #imgplot = plt.imshow(np.clip(data * factor, *clip_range))
        #plt.show()
        # Create compressed file
        keyfile = open(key_file, "rb")
        key = keyfile.read()
        cipher = AES.new(key, AES.MODE_SIV)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        file = open(encrypted_file_name, 'wb')
        file.write(ciphertext)
        file.close()

