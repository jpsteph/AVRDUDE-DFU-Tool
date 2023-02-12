
import os
import subprocess
import shutil

def main(projName = str, comPort = str):

    #binary to be DFU'd
    binName = projName + '.hex'
    #assuming this python file with be located in the Atmel Studio folder
    localDir = os.path.dirname(__file__)

    #creating paths to move hex file
    localDirBin = os.path.join(localDir, binName)
    dst = localDirBin.replace('\\', '/')

    binPath =  os.path.join(localDir, '7.0', projName, projName, 'Debug', binName)
    src = binPath.replace('\\', '/')

    #if hex file is here from a previous DFU, delete it
    if(os.path.isfile(dst)):
        os.remove(dst)

    #copy hex file to DFU directory
    shutil.copyfile(src, dst)

    avrDudeCmd = 'avrdude -p m32u4 -P ' +  comPort + ' -c avr109 -U flash:w:' + binName
    print('Sending DFU cmd: ' + avrDudeCmd)
    p1 = subprocess.Popen(avrDudeCmd)
    p1.wait()
    
    #deleting hex file from DFU folder
    os.remove(dst)


if __name__ == "__main__":
    main(projName = 'radioproj400mhz', comPort = 'COM7')


