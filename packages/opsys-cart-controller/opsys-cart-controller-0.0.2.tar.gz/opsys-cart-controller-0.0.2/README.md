# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* This repository is a part of opsys automation infrastructure
* This repository is cart controller implementation for cart moving on rail

### How do I get set up? ###

* pip install opsys-cart-controller

### Unit Testing

* python -m unittest -v

### Usage Example
```
from opsys_cart_controller.cart_controller import CartController

cart = CartController()

cart.start_distance = 10
cart.end_distance = 15

cart.setup_cart_motor()
distance = cart.get_distance()
cart.move_to_start()
cart.move_to_end()
cart.move_cart_motor(dest=10)
```