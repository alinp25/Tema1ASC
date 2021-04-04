"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)

        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time

    def run(self):
        for cart in self.carts:
            cart_id = self.marketplace.new_cart()

            for op in cart:
                no_ops = 0

                # Extract the operation details
                qty = op["quantity"]
                op_type = op["type"]
                prod = op["product"]

                # If the operation is successful (the product is available)
                # then proceed to the next operation, otherwise wait for the
                # product to become available
                while no_ops < qty:
                    result = self.execute_operation(cart_id, op_type, prod)

                    if result is None or result:
                        no_ops += 1
                    else:
                        time.sleep(self.retry_wait_time)

            self.marketplace.place_order(cart_id)

    def execute_operation(self, cart_id, operation_type, product) -> bool:
        if operation_type == "add":
            return self.marketplace.add_to_cart(cart_id, product)

        if operation_type == "remove":
            return self.marketplace.remove_from_cart(cart_id, product)

        return False
