import pickle
import pandas as pd

model = pickle.load(open('./trained.pkl','rb'))
df = pd.read_csv('test.csv')
# df = df.head(100)
print(df.info())

z = []

for i,r in df.iterrows():
    x = [r['Process temp'],r['Rpm'],r['Torque'],r['Tool wear']]
    # x = [310, 2800, 60, 230]
    pred = model.predict([x])
    if pred == 1:
        z.append(pred)

print("Out of ",len(df)," test cases ",len(z), " failed")