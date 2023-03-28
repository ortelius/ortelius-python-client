import json
import unittest

from ortelius import transpose

denormalized_data = {}
with open("denormalized.json", mode="r", encoding="utf-8") as file_data:
    denormalized_data = json.load(file_data)

expected_normalized_data = [
    "ipfs://bafkreihcaehhl6k2ekd37dqaj6rqegdq5hcelr7ly4aupaenkqdm4wucfm",
    "ipfs://bafkreiezkbcsvmmskosikhwfgot6reopiu5yvx5zyu6xdjtonf3rvotzui",
    "ipfs://bafkreiff3yjhwwx4gbftm5rqkz5tj3us3wsltwkakb2wf4yjtezg7hcwvq",
    "ipfs://bafkreifvaabjhi67r4jzcx6t7jwa66bzfd33bna274rbgahf6qaodbma2m",
    "ipfs://bafkreids5svygibbwm36oj3ad3pj4ytna76dpwzmitlqboqnikwgultdou",
    "ipfs://bafkreigo3cgb6rgyab3rdwmbhhzlgt7e76aqso2rtipciwb67emri72ngq",
    "ipfs://bafkreibs7g5z74pzalzu5wumjtjdqhwnj5oju6ckwxwyj4yeoqeljrzfdy",
    "ipfs://bafkreid66tulb3whkoi42emjnzs7a7gkghfwuo6qawnb4ylpm5hma46ueu",
    "ipfs://bafkreiedeqhp4ygdciew6sbhayzhfr6h53zslzsouqg4wwypa2dxzvvjie",
    "ipfs://bafkreihq3vpleriegftlzdwbaqosxk77s6ekgkodmkrh2l7vtlic2f6qxm",
    "ipfs://bafkreihy46zj7y2a6y2f7bcyqc526ylqumn3gjv4lpnnsppdmweqpshhhi",
    "ipfs://bafkreiczajynwwrztwky7njmjebzgrbp7kmod23ymc32a5gzefdwt2mioq",
    "ipfs://bafkreic4ke5hq2inkchyefns4ruct6dgkegewbnizqv6ovndiza2ffmwb4",
    "ipfs://bafkreih5ukf7mae3fhou76mhkcnteh2gwfrmo6nq3c4skruk6gkl2e3fjy",
    "ipfs://bafkreicc7jaflfcjikbrjahaub6wj4hjyrduzk6wel3tszu23rcxtllrey",
    "ipfs://bafkreihkprgnvf36eww24vt6atwpje7nmrd3s34fa5e6potqv4h3smvxk4",
    "ipfs://bafkreic3qg3ii4eufyolyxlgaoxubu3ot74duuozm425g3pfymjdfijn6a",
    "ipfs://bafkreibubqkcfjk332beuehh2bx5o4wp7suydmbwx5rr63l2dyz2qy2wky",
    "ipfs://bafkreidisn5lptp7tuj2i5jwyjkfkrdf7jw3becp2fdmzpc2csvecswtx4",
    "ipfs://bafkreig437cug4pst2kocvhvrk5gxnzcir4h5hdfovrm7gd7aez3jfuata",
    "ipfs://bafkreicvnwz3kpoq2psykmqomchtikbyfmblzkli23nvnnilvyiccag3le",
    "ipfs://bafkreias5w55ugpw4dazmbo3jlazoyatuew5ac7klshnjwd4iidxcsbs6e",
]


class TestFuntionalCases(unittest.TestCase):
    def test_normalize(self):
        actual_normalized_data = transpose.normalize(denormalized_data)

        self.assertTrue(actual_normalized_data is not None)
        self.assertEqual(actual_normalized_data, expected_normalized_data)

    def test_de_normalize(self):
        actual_denormalized_data = transpose.de_normalize(expected_normalized_data)

        # Remove the _keys from the nested dictionaries since they are generated
        transpose.remove_key(actual_denormalized_data)
        transpose.remove_key(denormalized_data)

        self.assertTrue(actual_denormalized_data is not None)
        self.assertEqual(denormalized_data, actual_denormalized_data)


if __name__ == "__main__":
    unittest.main(warnings="ignore")
