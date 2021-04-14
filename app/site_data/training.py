import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

df = pd.read_csv("tool_data.csv")
df = df.head(6000)

features = ['Process temp', 'Rpm', 'Torque', 'Tool wear']
X = df[features]
y = df['Machine failure']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state=27)

# test = pd.DataFrame(X_test)
# test.to_csv('test.csv',index=False)
model = LogisticRegression()
train = model.fit(X_train, y_train)
# print(model.score(X_test,y_test))
# pickle.dump(train,open('trained.pkl','wb'))