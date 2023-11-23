import time
from .cart_abstract import CartAbstract
from cart.configs import *
import cart.motor_control as motor
import cart.laser_distance as laser
import cart.ps_params as ps


class CartController(CartAbstract):
    """
    Cart controller interface
    """
    def __init__(self):
        """
        Initialize parameters
        """
        self.laser_com = LaserConfigurations.COM       # LRF COM port number
        self.ps_com = PowerSupplyConfigurations.COM    # Motor PS COM port number
        self.deviation = CartConfigurations.DEVIATION  # Diff between measured and configured distance
        self.velocity = CartConfigurations.VELOCITY    # Cart motor velocity
        self.accel = CartConfigurations.ACCEL          # Motor acceleration
        self.decel = CartConfigurations.DECEL          # Motor Deceleration
        self.timeout = CartConfigurations.TIMEOUT      # Movement step timeout
        self.start_distance = 0                        # in meters
        self.end_distance = 0                          # in meters

    def setup_cart_motor(self):
        """
        Cart motor configs initialization
        """
        print("Setup cart motor")
        # init connections
        print("Initializing connections...")
        
        motor.init_com()
        laser.init_com(self.laser_com)
        ps.init_com(self.ps_com)
        print("Done!")
        
        # display PS params
        print("PS Voltage: ", ps.read_volt())
        print("PS Current: ", ps.read_current())

    def move_to_start(self):
        """
        Move cart to the start of the track
        """
        self.move_cart_motor(dest=self.start_distance)

    def move_to_end(self):
        """
        Move cart to the end of the track
        """
        self.move_cart_motor(dest=self.end_distance)

    def move_cart_motor(self, dest):
        """
        Move cart motor to given distance

        Args:
            dest (float): destination distance
        """
        # move to destination position
        print(f"\nMoving motor to {dest} m\n")
        
        target_pos = dest
        current_pos = self.get_distance()
        start_move = time.perf_counter()
        
        motor.abs_pos(self.laser_com, pos=target_pos,
                      velocity=self.velocity, accel=self.accel, decel=self.decel)
        
        dist_remain = target_pos - current_pos
        
        while not(dist_remain < self.deviation and dist_remain > - self.deviation):
            print("Distance remaining: ", round(dist_remain, 3))
            print("Current position: ", round(current_pos, 3))
            
            try:
                current_pos = self.get_distance()
                dist_remain = target_pos - current_pos
                
            except:
                laser.init_com(self.laser_com)
                print("Laser read failure, retrying...")
                
            end_move = time.perf_counter()
            
            if end_move - start_move > self.timeout:
                print("Stop cart - Timeout over")
                break
            
            time.sleep(1)

        time.sleep(1)
        current_pos = self.get_distance()
        
        print("Cart arrived! Current position is: ", current_pos)

    def get_distance(self):
        """
        Read cart current distance

        Returns:
            float: current cart distance
        """
        return laser.read_dist()

    def stop_cart(self):
        """
        Stop cart movement
        """
        print('Cart movement stopping...')
        motor.e_stop()
