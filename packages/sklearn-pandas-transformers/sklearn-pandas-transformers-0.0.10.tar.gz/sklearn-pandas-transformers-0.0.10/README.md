The main use of this package is to use Sklearn Pipeline with transformer / estimator that doesn't comply with the basic Pipeline:

1 - Use sklearn Pipeline with transformation on Y:

```
spliter = SplitXY("a")

pipe = Pipeline([
        ("imputer", SklearnPandasWrapper(KNNImputer())),
        ("spliter", spliter), ("scaler", StandardScaler()),
        ("rf",
            EstimatorWithoutYWrapper(RandomForestRegressor(random_state=45),
                                    spliter))
    ])
pipe.fit(self.input_df)

res = pipe.predict(self.input_df)
```

2 - Use sklearn Transformer (returning numpy array)  to return pandas DataFrame (with unchanged columns names):


```
SklearnPandasWrapper(StandardScaler()))
```
