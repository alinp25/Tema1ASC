"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Lock, currentThread


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """

        self.queue_size_per_producer = queue_size_per_producer
        self.products_mapping = {}  # maps the product to the producer
        self.producers_queues = []  # holds the queue count for each producer
        self.consumers_carts = {}  # holds the consumers carts
        self.available_products = []  # contains the available products
        # Number of carts required to be stored separately for thread-safety in
        # new carts creation
        self.no_carts = 0

        self.consumer_cart_creation_lock = Lock()
        self.cart_operation_lock = Lock()

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        new_producer_id = len(self.producers_queues)

        self.producers_queues.append(0)

        return new_producer_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """

        if self.producers_queues[producer_id] >= self.queue_size_per_producer:
            return False

        self.producers_queues[producer_id] += 1
        self.available_products.append(product)

        self.products_mapping[product] = producer_id

        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        with self.consumer_cart_creation_lock:
            self.no_carts += 1

            self.consumers_carts[self.no_carts] = []

            return self.no_carts

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        with self.cart_operation_lock:
            if product not in self.available_products:
                return False

            producer_id = self.products_mapping[product]
            self.producers_queues[producer_id] -= 1

            self.available_products.remove(product)

            self.consumers_carts[cart_id].append(product)

            return True

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """

        self.consumers_carts[cart_id].remove(product)
        self.available_products.append(product)

        with self.cart_operation_lock:

            producer_id = self.products_mapping[product]
            self.producers_queues[producer_id] += 1

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        products = self.consumers_carts.pop(cart_id, None)

        for product in products:
            print(currentThread().getName() + " bought " + str(product))

        return products
