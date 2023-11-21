# Compare Dataframes

## Description
This module provides functionality to compare two dataframes. It uses various distance functions and provides a tabulated result for easy interpretation.

## Example Usage
```python
import polars as pl
df = pl.DataFrame(
    {
        "a": ['21-03-2022', 'soccer', 'cricket'],
        "b": ["21-03-2022", 'soccer', "cricket"],
        "c": [1, 2, 3],
    }
)

df1 = pl.DataFrame(
    {
        "a": ['21-03-2022', 'soccer', 'cricket', 'baseball'],
        "b": ["21-03-2022", 'sucker', "cricket", 'man'],
        "c": [4, 2, 3, 4],
        
    }
)
from comparedf import comparedf
compared = comparedf.Compare(df, df1)
print(compared) # prints the tabulated result
compared.save_report("<PATH_TO_SAVE_REPORT>")
```


