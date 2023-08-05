The main use of this package is to use Sklearn Pipeline with transformer / estimator that doesn't comply with the basic Pipeline:

1 - Use sklearn Pipeline with transformation on Y:

```
from sklearn_pandas_transformers.transformers import SplitXY, EstimatorWithoutYWrapper, SklearnPandasWrapper

from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np

input_df = pd.DataFrame([[0, 1, 2, 3], [4, 5, 6, 7], [8, np.nan, 9, 10]])
input_df.columns = ["a", "b", "c", "d"]

spliter = SplitXY("a")

pipe = Pipeline([
        ("imputer", SklearnPandasWrapper(KNNImputer())),
        ("spliter", spliter), ("scaler", StandardScaler()),
        ("rf",
            EstimatorWithoutYWrapper(RandomForestRegressor(random_state=45),
                                    spliter))
    ])
pipe.fit(input_df)

res = pipe.predict(input_df)
```

2 - Use sklearn Transformer (returning numpy array)  to return pandas DataFrame (with unchanged columns names):


```
SklearnPandasWrapper(StandardScaler()))
```
