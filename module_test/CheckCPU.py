import os
 
# Return CPU temperature as a character string                                     
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))
 
if __name__ == '__main__':
    print('')
    print('CPU Temperature = '+getCPUtemperature())
    