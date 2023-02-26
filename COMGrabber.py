import serial.tools.list_ports

def get_com(keyword, prin = None, cyclenum = None):
    cp = serial.tools.list_ports.comports()
    portlst = []
    #getting comport(s) (filtering by keyword)
    for p in cp:
        #displays com port info if 
        if prin != None:
            print(str(p))
        #if more than one device return a list
        # NOT TESTED     
        if cyclenum != None:
            if keyword in str(p):
                portlst.append(p.name)
        else:
            if keyword in str(p):
                start_of_address=p.hwid.rfind("&")
                end_of_address=p.hwid.rfind("_")
                address=p.hwid[start_of_address+1:end_of_address]
                port = p.name
                return port 
                #debug
                #print(p.name, address, port_type)
    return portlst
            

#testing multiple LFMS at once
"""
comlst = get_com('Prolific', prin = True, cyclenum = True)
slst = []
import serComm
import time

for index, c in enumerate(comlst):
    slst.append(serComm.serComm())
    slst[index].start_up(c, 38400)
    time.sleep(1)
    slst[index].write_read('txp')

print(slst)

"""







