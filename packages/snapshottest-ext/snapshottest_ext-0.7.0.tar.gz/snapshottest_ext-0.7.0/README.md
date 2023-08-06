# snapshottest_ext

extra formatter for snapshottest

## Usage

```python
# use with pytest
import pandas as pd
from snapshottest_ext.dataframe  import PandasSnapshot

def test_format(snapshot):
    df = pd.DataFrame([['a', 'b'], ['c', 'd']],
                      columns=['col 1', 'col 2'])
    snapshot.assert_match(PandasSnapshot(df))
```
