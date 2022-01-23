import pandas as pd
import sklearn
import xgboost as xgb





df = pd.DataFrame([[1,2]],
                  columns = ['A', 'B']
                  )
print(df)




print("Pandas version = " +(pd.__version__))
print("xgboost version = " +(xgb.__version__))
print("Scikit learn version = " +(sklearn.__version__))

print("Congrats, your environmnet works well !")