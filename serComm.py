import serial
import time

class serComm:
    def start_up(self, comPort, baudrate, timeout = None):
        try:
            if timeout == None:
                self.ser = serial.Serial(comPort, baudrate, bytesize = 8, parity = 'N', stopbits = 1,timeout = 1)
            else:
                self.ser = serial.Serial(comPort, baudrate, bytesize = 8, parity = 'N', stopbits = 1,timeout = timeout)
            self.ser.close()
            self.ser.open()
        except:
            print('Serial Port cannot be accessed!')

    #serially writes input and reads response after delay 
    def write_read_newline(self, input = None, delay = None):
        if input != None:
            self.ser.write(bytes(input + '\n', 'utf-8'))
            #standard delay
            if delay == None:
                time.sleep(.0001)
            else:
                time.sleep(delay)
            response = self.ser.readlines(100)
            #attempt to flush data buffer
            self.ser.reset_output_buffer()
            self.ser.reset_input_buffer()
            #print(response)
            #printing empty line
            print('')
            time.sleep(.1)
            return response
        else:
            print('Incorrect Input!')

    def write(self, input = None, delay = None):
        if input != None:
            self.ser.write(bytes(input + '\r', 'utf-8'))
        if delay == None:
            time.sleep(.1)
        else:
            time.sleep(delay)
    
    def write_multiple(self, inputlst = list, delay = None):
        for cmd in inputlst:
            self.ser.write(bytes(cmd + '\r', 'utf-8'))
            if delay == None:
                time.sleep(.1)
            else:
                time.sleep(delay)

    def CR(self, delay = None):
        self.ser.write(bytes('\r\n', 'utf-8'))
        if delay == None:
            time.sleep(.1)
        else:
            time.sleep(delay)    

    def close_port(self):
        self.ser.close()

    #serially writes input and reads response after delay 
    def write_read(self, input = None, delay = None):
        if input != None:
            self.ser.write(bytes(input + '\r', 'utf-8'))
            self.ser.reset_output_buffer()
            self.ser.reset_input_buffer()
            #standard delay
            if delay == None:
                time.sleep(.1)
            else:
                time.sleep(delay)
            response = self.ser.readlines(100)
            #attempt to flush data buffer
            self.ser.reset_output_buffer()
            self.ser.reset_input_buffer()
            print(response)
            #printing empty line
            print('')
            time.sleep(.1)
            return response
        else:
            print('Incorrect Input!')

    def wait_read(self, delay = None, chars = None, prints = None):
        self.ser.reset_output_buffer()
        
        if delay != 0:
            time.sleep(delay)
        if chars != None:
            response = self.ser.readlines(chars)
        else:
            response = self.ser.readlines(50)
        if prints != None:
            print(response)
        
        return response
    
    def clear_input_output_buffer(self):
        self.ser.reset_output_buffer()
        self.ser.reset_input_buffer()
    
    #writes two exclamation marks to the LFM to wake it up from sleep mode
    def LFM_wakeup(self):
        self.ser.write(bytes('!\r', 'utf-8'))
        time.sleep(.2)
        self.ser.write(bytes('!\r', 'utf-8'))
        

    #misc function for parsing S/N for LFM to make the Excel sheet title  
    def str_parser_LFM_SN(self, s):
        s = str(s)
        #get rid of b'
        s = s[2:len(s)]

        #if byte ends in :.' skip the deletion 
        if s.count(":.'") > 0:
            pass
        else:
            #get rid of \r\n'
            s = s[0:len(s) - 5]

        s = s.replace('/','-')
        return s

    def str_parser_LFM(self, s):
        s = str(s)
        #get rid of b'
        s = s[2:len(s)]

        #if byte ends in :.' skip the deletion 
        if s.count(":.'") > 0:
            pass
        else:
            #get rid of \r\n'
            s = s[0:len(s) - 5]
        return s

    def get_temp(self, device = None):
        if device == None or device == 'New LFM':
            var = 5
        elif device == 'Old LFM':
            var = 0

        temp = self.write_read(input = 'tmpi 0', delay = .1)
        try:
            temp = self.str_parser_LFM(temp[1])
            tempF = float(temp[0:5]) * 9/5 + 32
            print(str(tempF - var) + ' F')
        except:
            self.get_temp()
        try:
            return tempF
        except:
            pass


    def BER_parse(self, BERstr):
        #test case
        #BERstr = 'ErrBits: 00000510 BitCnt: 0000001104 BER: 4.619565e-01'

        BERarr = [None] * 2

        count = 0
        for s in BERstr.split():
            if s.isdigit():
                BERarr[count] = s
                count += 1

        #gets rid of most significant zeroes
        for sindex, s in enumerate(BERarr):
            for charindex, char in enumerate(s):
                if char == '0':
                    pass
                else: 
                    BERarr[sindex] = s[charindex : len(s)]
                    break

        BitER = float(BERarr[0]) / float(BERarr[1])
        print('Bit Error : ' + str(BitER * 100) + ' %')
        return BitER, float(BERarr[1])

            #parses LFM serial response for a number and converts it from byte to float
    def byte_parser(self, byte):
        l = []
        for t in str(byte):
            #case for preserving negative sign of negative number
            if t == '-' and len(l) == 0:
                l.append(t)
            #case for preserving decimal values of the number 
            if t == '.':
                l.append(t)
            #if it isn't a number don't add it to the list 
            try:
                l.append(int(t))
                #converts int to string for join operation at the end 
                l[len(l) - 1] = str(l[len(l) - 1])
            except ValueError:
                pass
        #convert list with only string entries to float
        fl = float(''.join(l))
        return fl

    def write_BER(self, BERdelay):
        while True:
            self.write(input = '\r', delay = .5)
            self.write(input = 'ber', delay = BERdelay)
            self.clear_input_output_buffer()
            self.write(input = '\r')
            self.wait_read(delay = .5)
            response = self.wait_read(delay = .5)
            try:
                bitError, bitTotal = self.BER_parse(response[2])
                return bitError, bitTotal
            except:
                print('\nBER Result Invalid, Attempting another BER Serial Command\n')

    def write_si(self):
        time.sleep(1)
        response = self.write_read(input = 'si', delay = .1)
        while True:
            try:
                response = self.byte_parser(response)
                if response == None or response == 0:
                    raise ValueError
                intr = int(response) 
                return response
            except:
                print('\nSI Result Invalid, Attempting another SI Serial Command\n')
                time.sleep(1)
                response = self.write_read(input = 'si', delay = .1)


