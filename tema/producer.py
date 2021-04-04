"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)

        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time

        # Generate the producer's id
        self.producer_id = self.marketplace.register_producer()

    def run(self):
        # Continuously generate products that are placed in the marketplace
        while True:
            for (product, no_products, publish_wait_time) in self.products:
                no_prod = 0

                while no_prod < no_products:
                    result = self.publish_product(product, publish_wait_time)

                    if result:
                        no_prod += 1

    def publish_product(self, product, publish_wait_time) -> bool:
        """
        Publish product to marketplace.

        @type product: Product
        @param product: the product to be published to the marketplace

        @type publish_wait_time: float
        @param publish_wait_time: the wait time needed for the product to be published
        """
        result = self.marketplace.publish(self.producer_id, product)

        # If the publish was successful start move to the next product, otherwise
        # wait until the queue gets freed and the publish is available to happen
        if result:
            time.sleep(publish_wait_time)
            return True

        time.sleep(self.republish_wait_time)
        return False
