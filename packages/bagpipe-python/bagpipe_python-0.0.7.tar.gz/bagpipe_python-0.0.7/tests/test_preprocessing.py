import unittest
import pandas as pd
from bagpipe.preprocessing import ApplyThreshold


class TestApplyThreshold(unittest.TestCase):
    def setUp(self):
        self.transformer = ApplyThreshold(by="value", threshold=5)

    def test_threshold_condition(self):
        df = pd.DataFrame({"value": [1, 2, 3, 4, 5, 6, 7, 8, 9]})
        expected_result = pd.Series(
            [False, False, False, False, False, True, True, True, True]
        )
        result = self.transformer._threshold_condition(df)
        pd.testing.assert_series_equal(result, expected_result)

    def test_process_group(self):
        df = pd.DataFrame({"value": [1, 2, 3, 4, 5, 6, 7, 8, 9]})
        expected_result = df
        result = self.transformer._process_group(df)
        pd.testing.assert_frame_equal(result, expected_result)

    def test_transform(self):
        df1 = pd.DataFrame({"value": [1, 2, 3, 4, 5, 6, 7, 8, 9]})
        df2 = pd.DataFrame({"value": [10, 20, 30, 40, 50, 60, 70, 80, 90]})
        dflist = [df1, df2]
        expected_result = [df1[df1["value"] > 5], df2]
        result = self.transformer.transform(dflist)
        for res, exp in zip(result, expected_result):
            pd.testing.assert_frame_equal(res, exp)


if __name__ == "__main__":
    unittest.main()
