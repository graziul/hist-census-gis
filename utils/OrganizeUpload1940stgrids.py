import os, sys
import pandas as pd
import paramiko

#path = '/s4-data/LatestCities/'
path = "C:\\Users\\cgraziul\\Documents\\Downloads\\"
stgrid_csv = path + 'Street Grid Progress (1940) - Sheet1.csv'
df = pd.read_csv(stgrid_csv)

username = "cgraziul"
password = "Tb82k#9v!G"
#username = sys.argv[1]
#password = sys.argv[2]

ssh = paramiko.SSHClient()
ssh.load_host_keys(os.path.expanduser(os.path.join("~",".ssh", "known_hosts")))
ssh.connect('rhea.pstc.brown.edu',username=username,password=password)
sftp = ssh.open_sftp()
sftp.put(localpath,removepath)
sftp.close()
ssh.close()
