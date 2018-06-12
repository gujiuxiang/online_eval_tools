import os
import shutil
directory = 'users'
outdirs = [dI for dI in os.listdir(directory) if os.path.isdir(os.path.join(directory,dI))]
for dir in outdirs:
    if os.path.isdir(directory + '/' + dir + '/result/'):
        shutil.rmtree(directory + '/' + dir + '/result/')
    os.mkdir(directory + '/' + dir + '/result/')
    if os.path.isdir(directory + '/' + dir + '/on_hold.json'):
        os.remove(directory + '/' + dir + '/on_hold.json')