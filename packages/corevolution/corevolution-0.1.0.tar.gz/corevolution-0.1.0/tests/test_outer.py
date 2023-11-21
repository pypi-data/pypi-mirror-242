import unittest

from corevolution.linalg import outer

class OuterTest(unittest.TestCase):
    
    test_1 = [1, 1, 0, 0, 0]
    test_2 = [0, 1, 0, 1, 0]

    def test_outer(self) -> None:
        
        compare = [[0, 1, 0, 1, 0], [0, 1, 0, 1, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
        result = outer(self.test_1, self.test_2)
        assert compare == result

if __name__ == "__main__": 
    unittest.main()