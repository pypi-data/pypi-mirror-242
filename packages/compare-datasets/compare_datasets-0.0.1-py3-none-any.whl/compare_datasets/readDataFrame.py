import polars as pl 
from collections import namedtuple

class compareDataFrames:
    """
    This class encapsulates the methods to compare two dataframes.

    Args:
        tested (polars.DataFrame): The dataframe to be tested.
        expected (polars.DataFrame): The expected dataframe.
        key (str): The column name to sort the dataframes.
        cast_numeric (bool, optional): Whether to cast numeric columns to a common type. Defaults to True.
        tolerance (int, optional): The numeric tolerance for comparison. Defaults to 6.

    Attributes:
        tested (polars.DataFrame): The dataframe to be tested.
        expected (polars.DataFrame): The expected dataframe.
        _tolerance (int): The numeric tolerance for comparison.
        _numeric_types (list): A list of numeric types for casting columns.
        _result (dict): A dictionary to store the comparison result.
        _mistmatched_schema (dict): A dictionary to store information about mismatched schemas.
        _row_and_column_counts (polars.DataFrame): A dataframe to store row and column counts.

    Methods:
        test_counts(): Compares the number of columns and rows between the dataframes.
        test_column_names(): Compares the column names between the dataframes.

    """
    def __init__(self, tested, expected, key, cast_numeric=True, tolerance=6):
        self.tested = tested.sort(key, descending=False)
        self.expected = expected.sort(key, descending=False)
        self._tolerance = tolerance
        self._numeric_types = [pl.Int64, pl.Float64, pl.UInt64, pl.Int32, pl.Float32, pl.UInt32, pl.Int16, pl.UInt16, pl.Int8, pl.UInt8]
        self._result = {}
        self._mistmatched_schema = {}
        self._row_and_column_counts = pl.DataFrame()
        self.report = {}

    def test_counts(self):
        """
        Compares the number of columns and rows between the dataframes.

        Returns:
            polars.DataFrame: A dataframe containing the counts and the difference between expected and tested dataframes.
        """
        row_and_column_counts = {
            "Attributes": ["No of columns", "No of rows"],
            "Expected": [len(self.expected.columns), len(self.expected)],
            "Tested": [len(self.tested.columns), len(self.tested)],
            "Difference (Expected - Tested)": [len(self.expected.columns) - len(self.tested.columns), len(self.expected) - len(self.tested)]
        }
        self._result['count_result'] = sum(row_and_column_counts["Difference (Expected - Tested)"]) == 0
        self._row_and_column_counts = pl.DataFrame(row_and_column_counts)
        return self._row_and_column_counts

    def test_column_names (self):
      """
      Compares the column names between the expected and tested dataframes.

      Returns:
          collections.namedtuple: A named tuple containing three sets: 
                                  - absent_columns_in_tested: Columns present in the expected dataframe but not in the tested dataframe.
                                  - absent_columns_in_expected: Columns present in the tested dataframe but not in the expected dataframe.
                                  - common_columns_in_both: Columns present in both the expected and tested dataframes.
      """
      absent_columns_in_tested = set(self.expected.columns) - set(self.tested.columns)
      absent_columns_in_expected = set(self.tested.columns) - set(self.expected.columns)
      common_columns_in_both = set(self.expected.columns).intersection(set(self.tested.columns))
      result = namedtuple('Result', 'absent_columns_in_tested absent_columns_in_expected common_columns_in_both')
      self.report['column_report'] = f"Columns in expected but not in tested: {absent_columns_in_tested}\nColumns in tested but not in expected: {absent_columns_in_expected}\nCommon columns in both: {common_columns_in_both}"      
      return result(absent_columns_in_tested, absent_columns_in_expected, common_columns_in_both)
    

    
    
    
    
    
    
      
    
    
      
      