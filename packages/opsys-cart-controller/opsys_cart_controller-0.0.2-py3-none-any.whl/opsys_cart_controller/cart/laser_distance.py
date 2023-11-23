import serial
from time import sleep
from configs import LaserConfigurations


SER_CONN = None


def init_com(com_port):
    """
    Initialize COM port session with laser

    Args:
        com_port (int): COM port number
    """
    try:
        global SER_CONN
        
        SER_CONN = serial.Serial('COM' + str(com_port), 
                                 LaserConfigurations.BAUDRATE, 
                                 timeout=LaserConfigurations.COM_TIMEOUT
                                 )
        SER_CONN.rts = True
        
        sleep(0.1)
        SER_CONN.rts = False
        sleep(3)
        
        SER_CONN.flushInput()
        SER_CONN.flushOutput()
        
    except Exception as e:
        print(f'Initializing laser COM error: {e}')
        raise


def close_com():
    """
    Close COM port session with laser
    """
    try:
        global SER_CONN
        
        if SER_CONN is not None:
            SER_CONN.close()
            SER_CONN = None
            
    except Exception as e:
        print(f'Laser disconnect error: {e}')
        raise


def read_dist():
    """
    Read distance from laser

    Returns:
        float: distance round value in meters
    """
    try:
        global SER_CONN
        
        if SER_CONN is None:
            raise ConnectionError('Must initialize COM port before reading!')
        
        read_cmd = b'\xAA\x00\x00\x20\x00\x01\x00\x00\x21'
        SER_CONN.write(read_cmd)
        reply = SER_CONN.read(13)
        dist = int.from_bytes(reply[6:10], 'big')  # returns value in mm
        
        return round(dist / 1000, 3)
    
    except Exception as e:
        print(f'Distance read error: {e}')
        raise



