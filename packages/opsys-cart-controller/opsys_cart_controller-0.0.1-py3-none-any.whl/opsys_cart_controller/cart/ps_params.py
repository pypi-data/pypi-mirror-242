import serial
from time import sleep
from configs import PowerSupplyConfigurations


SER_CONN = None


def init_com(com_port):
    """
    Initialize COM port session with PS

    Args:
        com_port (int): COM port number
    """
    global SER_CONN
    try:
        SER_CONN = serial.Serial('COM' + str(com_port), 
                                 PowerSupplyConfigurations.BAUDRATE, 
                                 parity=serial.PARITY_EVEN, 
                                 timeout=PowerSupplyConfigurations.COM_TIMEOUT
                                 )
        
        sleep(0.1)
        
        SER_CONN.flushInput()
        SER_CONN.flushOutput()
        
    except Exception as e:
        print(f'Initializing PS COM error: {e}')
        raise


def close_com():
    """
    Close com port session with PS
    """
    global SER_CONN
    
    try:
        if SER_CONN is not None:
            SER_CONN.close()
            SER_CONN = None
            
    except Exception as e:
        print(f'PS disconnect error: {e}')
        raise


def read_volt():
    """
    Read voltage from power supply

    Returns:
        float: PS voltage in Volts
    """
    global SER_CONN
    
    try:
        if SER_CONN is None:
            raise ConnectionError('Must initialize COM port before reading!')
        
        volt_cmd=b'\x01\x04\x00\x01\x00\x01\x60\x0A'
        SER_CONN.write(volt_cmd)
        sleep(0.1)
        reply = SER_CONN.read(8)
        a_val = int.from_bytes(reply[3:5],'big')  # analog value 0-1024. 1024==48V
        
        return round((a_val * 48) / 1024, 2)
    
    except Exception as e:
        print(f'PS voltage read error: {e}')
        raise


def read_current():
    """
    Read current from power supply

    Returns:
        float: PS current in Ampers
    """
    global SER_CONN
    
    try:
        if SER_CONN is None:
            raise ConnectionError('Must initialize COM port before reading!')
        
        curr_cmd = b'\x01\x04\x00\x02\x00\x01\x90\x0A'
        SER_CONN.write(curr_cmd)
        sleep(0.1)
        reply = SER_CONN.read(8)
        a_val = int.from_bytes(reply[3:5], 'big') # analog value 0-1024. 1024==12.5A
        
        return round((a_val * 12.5) / 1024, 2)
    
    except Exception as e:
        print(f'PS current read error: {e}')
        raise
