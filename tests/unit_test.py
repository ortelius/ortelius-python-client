import json
import unittest

from ortelius import transpose

expected_normalized_data = [
    "ipfs://bafkreib2tytdqwtl7xzqksbxwbqvrmkbo55n6m2ivglikchgiv5gwte2si",
    "ipfs://bafkreiawq3zb2dhvmwxys7glkgmv5qokw4fnlfbkw45tcj4uku5kc3dlqu",
    "ipfs://bafkreia7u7dd3wkjdrjgjxpy37vczpay2ewamddssaadwk3rf7xp7bams4",
    "ipfs://bafkreie2bh7jb3irvlllbnurvzakaeqwhmie4rv6sdhhnnev4rbs4eis6q",
    "ipfs://bafkreie4lc5k4djdyiukgiqhigxpenrjqjslq6gxmin5m62qtmxo3b4sgm",
    "ipfs://bafkreig3hlhk63fbwpvny6nou3uip7nhyxlznvygqietsqzkgxrdjuy6sa",
    "ipfs://bafkreig7jlcdg2akflzagtuxjcdnvn3osujcdyfewz5hyuzjlgj4bhu3fe",
    "ipfs://bafkreiaxh4sof5bb3vafa2g4u6jyledtlzqeodx47375skudetnemvs5pi",
    "ipfs://bafkreiffv2oxypru3uhphct62mif2meit22qnutjks52hbfoyoo4tmpkva",
    "ipfs://bafkreigh5ownbcgr7yuoarif6rpg2t2erdepxynkmbq6dwwaccy4i5di7y",
    "ipfs://bafkreicsa5m76prub2wjufmjq64kgu5i3rtl2en2pdhnfxcw465vkxib3m",
    "ipfs://bafkreieyxidpwmyxedtpeyx3qqa43oqftafpzd4bzptkkjjga3zttf6xma",
    "ipfs://bafkreig3yxvgitjwyvopbdnisfwzsv52spzg2wo64ff2qgrtrmayhzkm5q",
    "ipfs://bafkreiclh65ndhpy23b3xgyldprfbvodmxekm5sua2kdsxx74g552zqbei",
    "ipfs://bafkreiblgc5agtbkcaml3lvsh6uyddbztbaw6lvdi3xagpwsl3rh265jyu",
    "ipfs://bafkreid2hp5d6exbu72nry4czbybdzqya7jjqpogn3icfnakvw2bec4l7m",
    "ipfs://bafkreibgv2uqxpzm46xzp7c3tzhlvgr4eqgdfvg6qowhr35g5ahcn2ezrm",
    "ipfs://bafkreiefbcqplideg5olwlgwr5facruqx5dw6l3xfvk5gfgugh3eeezvka",
    "ipfs://bafkreifi3gguluv3picevgs3kelcjs4pavliew6yxxg6sib2obu4u52fvi",
    "ipfs://bafkreidxtnprnf7ddmmclf3aheyoij5zvyiruegiv5h2b2bhkup24y4mkm",
    "ipfs://bafkreihp5dlc7kg72fc6b2iqnhfswugw5urby57hdchnlpvacmnopnwkty",
    "ipfs://bafkreib5gp4tvg7xvvusyu36hlisudprsimundazqu4k74bx67ecoohapq",
]


class TestFuntionalCases(unittest.TestCase):
    def test_100_normalize(self):
        denormalized_data = {}
        with open("denormalized.json", mode="r", encoding="utf-8") as file_data:
            denormalized_data = json.load(file_data)

        actual_normalized_data = transpose.normalize(denormalized_data)

        self.assertTrue(actual_normalized_data is not None)
        self.assertEqual(actual_normalized_data, expected_normalized_data)

    def test_200_de_normalize(self):
        denormalized_data = {}
        with open("denormalized.json", mode="r", encoding="utf-8") as file_data:
            denormalized_data = json.load(file_data)

        actual_denormalized_data = transpose.de_normalize(expected_normalized_data)

        # Remove the _keys from the nested dictionaries since they are generated
        transpose.remove_key(actual_denormalized_data)
        transpose.remove_key(denormalized_data)

        self.assertTrue(actual_denormalized_data is not None)
        self.assertEqual(denormalized_data, actual_denormalized_data)


if __name__ == "__main__":
    unittest.main(warnings="ignore")
