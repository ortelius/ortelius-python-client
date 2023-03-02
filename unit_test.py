import unittest

from storage_utils import *
from ortelius_common import *


f = open('./denormalized.json')
denormalized_data = json.load(f)
expected_normalized_data = ['ipfs://bafkreihcaehhl6k2ekd37dqaj6rqegdq5hcelr7ly4aupaenkqdm4wucfm', 'ipfs://bafkreiezkbcsvmmskosikhwfgot6reopiu5yvx5zyu6xdjtonf3rvotzui', 'ipfs://bafkreiff3yjhwwx4gbftm5rqkz5tj3us3wsltwkakb2wf4yjtezg7hcwvq', 'ipfs://bafkreifvaabjhi67r4jzcx6t7jwa66bzfd33bna274rbgahf6qaodbma2m', 'ipfs://bafkreids5svygibbwm36oj3ad3pj4ytna76dpwzmitlqboqnikwgultdou', 'ipfs://bafkreigo3cgb6rgyab3rdwmbhhzlgt7e76aqso2rtipciwb67emri72ngq', 'ipfs://bafkreibs7g5z74pzalzu5wumjtjdqhwnj5oju6ckwxwyj4yeoqeljrzfdy', 'ipfs://bafkreid66tulb3whkoi42emjnzs7a7gkghfwuo6qawnb4ylpm5hma46ueu', 'ipfs://bafkreiedeqhp4ygdciew6sbhayzhfr6h53zslzsouqg4wwypa2dxzvvjie', 'ipfs://bafkreihq3vpleriegftlzdwbaqosxk77s6ekgkodmkrh2l7vtlic2f6qxm', 'ipfs://bafkreihy46zj7y2a6y2f7bcyqc526ylqumn3gjv4lpnnsppdmweqpshhhi', 'ipfs://bafkreiczajynwwrztwky7njmjebzgrbp7kmod23ymc32a5gzefdwt2mioq', 'ipfs://bafkreic4ke5hq2inkchyefns4ruct6dgkegewbnizqv6ovndiza2ffmwb4', 'ipfs://bafkreih5ukf7mae3fhou76mhkcnteh2gwfrmo6nq3c4skruk6gkl2e3fjy', 'ipfs://bafkreicc7jaflfcjikbrjahaub6wj4hjyrduzk6wel3tszu23rcxtllrey', 'ipfs://bafkreihkprgnvf36eww24vt6atwpje7nmrd3s34fa5e6potqv4h3smvxk4', 'ipfs://bafkreic3qg3ii4eufyolyxlgaoxubu3ot74duuozm425g3pfymjdfijn6a', 'ipfs://bafkreigz4zkptri6qvrtodygetueym7lmj5wfnw5grezcs23khlkvteqxq', 'ipfs://bafkreifui7t5i2lxbj2i3phvpzgausxbigjtmtalc57kmsi36xqsvnn3eu', 'ipfs://bafkreif6j55ofhssasdj6zspkr3lpr5gjwmbz6qralmdjnb34lfp2nmytq', 'ipfs://bafkreighxjgqu7lzrj3x4i3qeakeguiefsbq2mx52jgzzccsnapdtun7ci', 'ipfs://bafkreicuz7pg3gc4vhulsvyj5tzochkyhebtr4n6yuf7vvpkxlbjv6wjea']

class TestFuntionalCases(unittest.TestCase):

    def test_normalize(self):
        actual_normalized_data = normalize(denormalized_data)
        print(actual_normalized_data)
        self.assertTrue(actual_normalized_data != None)
        self.assertEqual(actual_normalized_data, expected_normalized_data)

    def test_de_normalize(self):
        actual_denormalized_data = de_normalize(expected_normalized_data)
        print(actual_denormalized_data)
        self.assertTrue(actual_denormalized_data != None)
        self.assertEqual(denormalized_data, actual_denormalized_data)

if __name__ == '__main__':
    unittest.main(warnings='ignore')