from sprite import *


class CreateAd:
    def __init__(self, x, y, available_products):
        self.x = x
        self.y = y
        self.available_products = available_products
        self.ad = Actor('ad_empty', pos=(x, y))
        self.ad.scale = 2
        self.products = random.randint(1, 4)    # Randomization of product quantities
        self.products_list = []         # list of products
        self.amount_list = []           # Lista of amounts
        self.new_ad = {'ad': self.ad, 'do_it': None, 'items': [], 'amount': self.amount_list, 'prize': 0}  # Słownik do zwrócenia

    def check_list(self):
        keys = [key for key in self.available_products]
        product = random.randint(0, len(self.available_products) - 1)
        if keys[product] not in self.products_list:
            self.products_list.append(keys[product])
        else:
            self.check_list()

    def lottery(self):
        for i in range(self.products):      # Product randomization
            self.check_list()

        for i in range(self.products):      # Randomization of the quantity of each product
            i = random.randint(1, 10)
            self.amount_list.append(i)

    def calculate_the_prize(self):
        for index, product in enumerate(self.products_list):
            self.new_ad['prize'] += (self.available_products[product] * self.amount_list[index])

    def add_ad(self):
        self.lottery()
        self.calculate_the_prize()
        for index, product in enumerate(self.products_list):    # adding products in designated positions
            add = Actor(product, pos=(self.ad.x - self.ad.width / 2.6, self.ad.y))
            add.scale = 3
            self.new_ad['items'].append(add)

        return self.new_ad
