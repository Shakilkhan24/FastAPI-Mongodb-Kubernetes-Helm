import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt
import seaborn as sns

client = MongoClient('mongodb://localhost:27017/')
db = client['Project']
collection = db['Heart Disease']

data=collection.find()
df=pd.DataFrame(data)

sns.pairplot(df)
plt.title('pairplot')
plt.show()

