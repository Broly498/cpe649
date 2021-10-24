import ftplib

ftp_server = ftplib.FTP()
# Note: You will need to modify ip/port/credentials for
# whatever FTP server you configure. Also remember to
# create a mount point for the virtual path '/'.
# Also remember you will probably have to disable windows defender firewall for FTP server on windows.
ftp_server.connect('192.168.1.9',21)
ftp_server.login('user','password')
ftp_server.dir()
