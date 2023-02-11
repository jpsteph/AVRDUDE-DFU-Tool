
import os
import subprocess
from threading import Thread
from _thread import interrupt_main
from signal import signal
from signal import SIGINT
from time import sleep

def main(projName = str, comPort = str):

    #binary to be DFU'd
    binName = projName + '.hex'
    #assuming this python file with be located in the Atmel Studio folder
    localDir = os.path.dirname(__file__)

    #creating paths to move hex file
    localDirBin = os.path.join(localDir, binName)
    localDirFixed = localDirBin.replace('\\', '/')

    #if os.path.exists(localDirFixed):
    #    print('LOL')

    binPath =  os.path.join(localDir, '7.0', projName, projName, 'Debug', binName)
    binPathFixed = binPath.replace('\\', '/')

    os.rename(binPathFixed, localDirFixed)

    #register the signal handler for this process
    #signal(SIGINT, handle_sigint)
    #start the new thread
    #thread = Thread(target=task)
    #thread.start()

    avrDudeCmd = 'avrdude -p m32u4 -P ' +  comPort + ' -c avr109 -U flash:w:' + binName
    print('Sending DFU cmd: ' + avrDudeCmd)
    subprocess.Popen(avrDudeCmd)

    sleep(15)
    
    #moving hex file back into debug folder
    os.rename(localDirFixed, binPathFixed)

# task executed in a new thread
def task():
    # block for a moment
    sleep(20)
    # interrupt the main thread -> go to handle_sigint
    interrupt_main()

# handle single
def handle_sigint(signalnum, frame):
    # terminate
    print('Microcontroller took too long to respond. Exiting...')

if __name__ == "__main__":
    main(projName = 'radioproj400mhz', comPort = 'COM7')


