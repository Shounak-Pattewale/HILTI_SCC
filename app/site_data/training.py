import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

df = pd.read_csv("tool_data.csv")
df = df.head(6000)
print(len(df))

features = ['Process temp', 'Rpm', 'Torque', 'Tool wear']
X = df[features]
y = df['Machine failure']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=11)

# test = pd.DataFrame(X_test)
# print("\nDataset length : ",len(y_test))
# c = []
# for y in y_test:
#     if y == 1:
#         c.append(y)

# print("Original count of failures : ",len(c),"\n")

# test.to_csv('test.csv',index=False)
print(len(X_test))
model = LogisticRegression()
train = model.fit(X_train, y_train)
print(model.score(X_test,y_test))

# pickle.dump(train,open('trained.pkl','wb'))