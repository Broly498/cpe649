import matplotlib.pyplot as plt
import numpy as np
import gzip as gz
from Crypto.Cipher import AES
import sys
import ftplib
import io
from PIL import Image

ftp_server = ftplib.FTP()
# Note: You will need to modify ip/port/credentials for 
# whatever FTP server you configure. Also remember to 
# create a mount point for the virtual path '/'.
# Also also remember you will probably have to disable
# windows defender firewall for FTP server on windows.
ftp_server.connect('192.168.1.13',21)
ftp_server.login('user','password')

# Factor and clip used to increase visibility for plotting
factor=3.5/255
clip_range=(0, 1)

file_name = "runtime_encrypted.bin"
key_file = "key_file.bin"

def file_size_readable(n, suffix="B"):
    for unit in ["","K","M","G"]:
        if n < 1024:
            return f"{n:.2f}{unit}{suffix}"
        n /= 1024

while True:
    print('''\nWelcome to the cloud detection FTP client!
    1) Display contents of the FTP server
    2) Display file sizes of data in the FTP server
    3) Process and display an image
    4) Process and store an image to jpg
    5) Process and store all images to jpg
    6-9) Quit''')
    choice = int(input("Enter choice: "))

    if choice == 1:
        ftp_server.dir()
    elif choice == 2:
        for file in ftp_server.nlst():
            file_size = "N/A"
            # Ensure path is a file, not directory
            try:
                ftp_server.cwd(file)
            except Exception as e:
                ftp_server.voidcmd("TYPE I")
                file_size = file_size_readable(ftp_server.size(file))
            print(f"{file:10} {file_size}")
    elif choice == 3 or choice == 4:
        data_num = input("Enter number for chosen data. Ex) For data_12.dat enter '12': ")
        data_file_name = "data_" + data_num + ".dat"
        try: 
            files = ftp_server.nlst()
        except:
            print("Error fetching files, directory may be empty")
        if data_file_name in files:
            print("Processing...")
            byteHolder = io.BytesIO()
            ftp_server.retrbinary('RETR ' + data_file_name, byteHolder.write)
            byteHolder.seek(0)
            encrypted_compressed_data = byteHolder.read()
            print("Encrypted/compressed data fetched. Size: " + str(sys.getsizeof(encrypted_compressed_data)))
            #Unencrypt the data
            #Get the tag
            tagfile = open("tag_" + data_num, "rb")
            tag = tagfile.read()
            #Get the key
            keyfile = open(key_file, "rb")
            key = keyfile.read()
            cipher = AES.new(key, AES.MODE_SIV)
            compressed_data = cipher.decrypt_and_verify(encrypted_compressed_data, tag)
            print("Data decrypted. Size: " + str(sys.getsizeof(compressed_data)))
            # Optional test, uncompress and display image
            uncompressed_data = io.BytesIO(gz.decompress(compressed_data))
            print("Data uncompressed. Size: " + str(sys.getsizeof(uncompressed_data)))
            uncompressed_image_data = np.load(uncompressed_data, allow_pickle=True)
            # For option 3, display plot. For option 4, store in file and upload to FTP server
            if choice == 3:
                print("Displaying image...")
                imgplot = plt.imshow(np.clip(uncompressed_image_data * factor, *clip_range))
                plt.show()
            elif choice == 4:
                img = Image.fromarray(uncompressed_image_data)
                f = io.BytesIO()
                img.save(f, format="jpeg")
                f.seek(0)
                ftp_server.storbinary('STOR image_' + str(data_num) + '.jpeg', f)
        else:
            print(data_file_name + " was not found.")
    elif choice == 5:
        try: 
            files = ftp_server.nlst()
        except:
            print("Error fetching files, directory may be empty")
        number_of_data_files = len([i for i in files if ".dat" in i])
        for data_num in range(1, number_of_data_files+1):
            data_file_name = "data_" + str(data_num) + ".dat"
            if data_file_name not in files:
                print(data_file_name + " was not found. Cannot convert to jpg")
                continue
            byteHolder = io.BytesIO()
            ftp_server.retrbinary('RETR ' + data_file_name, byteHolder.write)
            byteHolder.seek(0)
            encrypted_compressed_data = byteHolder.read()
            print("Encrypted/compressed data fetched. Size: " + str(sys.getsizeof(encrypted_compressed_data)))
            #Unencrypt the data
            #Get the tag
            tagfile = open("tag_" + str(data_num), "rb")
            tag = tagfile.read()
            #Get the key
            keyfile = open(key_file, "rb")
            key = keyfile.read()
            cipher = AES.new(key, AES.MODE_SIV)
            compressed_data = cipher.decrypt_and_verify(encrypted_compressed_data, tag)
            print("Data decrypted. Size: " + str(sys.getsizeof(compressed_data)))
            # Optional test, uncompress and display image
            uncompressed_data = io.BytesIO(gz.decompress(compressed_data))
            print("Data uncompressed. Size: " + str(sys.getsizeof(uncompressed_data)))
            uncompressed_image_data = np.load(uncompressed_data, allow_pickle=True)
            img = Image.fromarray(uncompressed_image_data)
            f = io.BytesIO()
            img.save(f, format="jpeg")
            f.seek(0)
            ftp_server.storbinary('STOR image_' + str(data_num) + '.jpeg', f)
    else:
        break
