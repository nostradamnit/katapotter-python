import unittest

# The Counter from the python standard library is a big asset in this kata
# http://docs.python.org/2/library/collections.html#collections.Counter
from collections import Counter


PRIX_UNITAIRE = 8
REDUCTION = {1: 1, 2: 0.95, 3: 0.90, 4: 0.80, 5: 0.75}
BOOK_COLLECTION_SIZE = 5
BOOKS = [1, 2, 3, 4, 5]


def bundle_books(cart):
    stacks = Counter(cart)
    bundles = []
    books = stacks.keys()

    # Edge cases are only present when the cart contains at least one of each book
    while len(stacks) == len(BOOKS):
        # Empty stacks from series until the quantity of one of the books is 1
        while all([quantity > 1 for quantity in stacks.values()]):
            bundles.append(books)
            stacks = stacks - Counter(BOOKS)

        # Make a bundle of 4 containing one orphan book
        bundle = []
        for i in range(4):
            book = books[i]
            orphan_added = False
            if stacks[book] > 1 or not orphan_added:
                bundle.append(book)
                if stacks[book] == 1:
                    orphan_added = True
                stacks = stacks - Counter({book: 1})
        if bundle:
            # Check if it's possible to make other bundles of 4 and a full serie
            # If the bundle of 4 is impossible but the serie is possible then make one
            not_in_bundle = (set(BOOKS) - set(bundle)).pop()
            if len(stacks) < 4 and not_in_bundle in stacks:
                bundle.append(not_in_bundle)
                stacks = stacks - Counter({not_in_bundle: 1})
            bundles.append(bundle)

    # Make bundle with the remaining books, the simplest way possible
    while sum(stacks.values()):
        bundle = []
        for book in stacks.keys():
            bundle.append(book)
            stacks = stacks - Counter({book: 1})
        bundles.append(bundle)
    return bundles


def get_price(cart):
    return sum([len(stack) * PRIX_UNITAIRE * REDUCTION[len(stack)]
                for stack in bundle_books(cart)])


class TestKataPotter(unittest.TestCase):
    def setUp(self):
        self.cart = []

    def test_2_series_missing_each_missing_one_are_separated_correctly(self):
        cart = [1] * 2 + [2] * 2 + [3] * 2 + [4] + [5]
        self.assertEqual(bundle_books(cart), [[1, 2, 3, 4], [1, 2, 3, 5]])

    def test_full_series_plus_some_single_books_are_separated_correctly(self):
        cart = BOOKS * 2 + [1] * 3
        self.assertEqual(bundle_books(cart), [
            BOOKS,
            BOOKS,
            [1], [1], [1]
        ])

    def test_un_livre_coute_8(self):
        self.cart.append(1)
        self.assertEqual(get_price(self.cart), 8)

    def test_deux_livres_coutes_16_euros_moins_5_pourcent(self):
        self.cart.append(1)
        self.cart.append(2)
        self.assertEqual(get_price(self.cart), 15.2)

    def test_deux_meme_livres_coutes_16_euros(self):
        self.cart.append(1)
        self.cart.append(1)
        self.assertEqual(get_price(self.cart), 16)

    def test_trois_livres_coutent_24_moins_dix_pourcent(self):
        self.cart.append(1)
        self.cart.append(2)
        self.cart.append(3)
        self.assertEquals(get_price(self.cart), 21.6)

    def test_quatre_livres_coutent_32_moins_vingt_pourcent(self):
        self.cart = [1, 2, 3, 4]
        self.assertEquals(get_price(self.cart), 25.6)

    def test_quatre_livres_identique_coutent_32(self):
        self.cart = [1, 1, 1, 1]
        self.assertEqual(get_price(self.cart), 32)

    def test_deux_paires_de_livres(self):
        self.cart = [1, 1, 2, 2]
        self.assertEquals(get_price(self.cart), 30.4)

    def test_deux_paires_plus_un_de_livres(self):
        self.cart = [1, 1, 2, 2, 3]
        self.assertEquals(get_price(self.cart), 36.8)

    def test_deux_1_deux_2_un_3_et_un_4(self):
        self.cart = [1, 1, 2, 2, 3, 4]
        self.assertEquals(get_price(self.cart), 40.8)

    def test_deux_1_deux_2_deux_3_un_4_et_un_5(self):
        self.cart = [1, 2, 3, 4, 1, 2, 3, 5]
        self.assertEquals(get_price(self.cart), 51.2)

if __name__ == "__main__":
    unittest.main()
