from unittest import TestCase
PRIX_UNITAIRE = 8
REDUCTION = { 1:1, 2:0.95, 3:0.90, 4:0.80, 5:0.75 }


def get_price(cart):
    prix_panier = 0
    while cart:
        book_set = set(cart)
        for book in book_set:
            cart.pop(cart.index(book))
        prix_panier += len(book_set) * PRIX_UNITAIRE * REDUCTION[len(book_set)]
    return prix_panier


class TestKataPotter(TestCase):
    def setUp(self):
        self.cart = []

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
        self.cart = [1,2,3,4]
        self.assertEquals(get_price(self.cart), 25.6)

    def test_quatre_livres_identique_coutent_32(self):
        self.cart = [0,0,0,0]
        self.assertEqual(get_price(self.cart),32)

    def test_deux_paires_de_livres(self):
        self.cart = [1,1,2,2]
        self.assertEquals(get_price(self.cart),30.4)


    def test_deux_paires_plus_un_de_livres(self):
        self.cart = [1,1,2,2,3]
        self.assertEquals(get_price(self.cart), 36.8)

    def test_deux_1_deux_2_un_3_et_un_4(self):
        self.cart = [1,1,2,2,3,4]
        self.assertEquals(get_price(self.cart), 40.8)

    def test_deux_1_deux_2_deux_3_un_4_et_un_5(self):
        self.cart = [1,1,2,2,3,3,4,5]
        self.assertEquals(get_price(self.cart), 51.2)
