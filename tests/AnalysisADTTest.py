import unittest
import pathlib
from os import path
import sys
sys.path.append("../src/database_convertion")
from AnalysisADT import SignPointProcess, SignPointArray

test_data = {
    'image_name': 'test.jpg',
    'initial_size_x': 10,
    'initial_size_y': 10,
    'country': 'SWEDEN',
    'occlusions': 'VISIBLE',
    'sign_class': 'PROHIBITORY',
    'sign_type': '120_SIGN'
}


class SignPointProcessTest(unittest.TestCase):

    def test_from_props(self):
        sign_point = SignPointProcess.from_props(**test_data)
        self.assertEqual(sign_point.image_name, bytes(test_data['image_name'], encoding='utf-8'))

    def test_to_repr(self):
        test_line = "img.jpg,100,50,GERMANY,VISIBLE,PROHIBITORY,120_SIGN"
        sign_point = SignPointProcess.to_repr(SignPointProcess.from_repr(test_line))
        self.assertEqual(sign_point, test_line)

    def test_from_repr(self):
        sign_point = SignPointProcess.from_repr("test.jpg,100,50,GERMANY,VISIBLE,PROHIBITORY,120_SIGN")
        self.assertEqual(sign_point.image_name, bytes(test_data['image_name'], encoding='utf-8'))


class SignPointArrayTest(unittest.TestCase):

    def setUp(self) -> None:
        self.arr = SignPointArray()
        self.tests_path = path.join(pathlib.Path(__file__).parent.absolute(), 'test_utils')

    def test_from_file(self):
        self.arr.from_file(path.join(self.tests_path, 'test_dataset.csv'))

        self.assertEqual(len(self.arr), 3)

    def test_add_entry(self):
        free_ind_before = self.arr._free_ind
        self.arr.add_entry(**test_data)
        self.assertTrue(free_ind_before + 1 == self.arr._free_ind)
        self.assertEqual(self.arr._rows[free_ind_before].image_name, bytes(test_data['image_name'], encoding='utf-8'))

    def test_to_file(self):
        tmp_path = path.join(self.tests_path, 'tmp.csv')
        self.arr.add_entry(**test_data)
        self.arr.to_file(tmp_path)

        with open(tmp_path) as f:
            content = f.read().strip()

        with open(tmp_path, 'w') as f:
            f.write('')

        self.assertEqual(content, SignPointProcess.to_repr(SignPointProcess.from_props(**test_data)))

    def test_enlarge(self):
        size_before = self.arr.__sizeof__()
        self.arr._enlarge()
        self.assertGreater(self.arr.__sizeof__(), size_before)


if __name__ == '__main__':
    unittest.main()
