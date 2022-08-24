from flask import Flask
import pickle
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import MinMaxScaler
#######
app = Flask(__name__)

@app.route("/")
def hello_world():
    df = pd.read_csv('clean_training_data.csv')
    nucols = [c for c in df.columns if c not in ('name','spread1','spread2','D2','RPDE','Jitter:DDP','Shimmer:DDA','DFA')]
    print('COLS=', nucols)
    df = df[nucols]
    labels = pd.read_csv('status.csv').values
    features = df.values

    scaler = MinMaxScaler((-1, 1))
    X = scaler.fit_transform(features)
    Y = labels
    model = pickle.load(open('model0.pk','rb'))
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.14, random_state=42)

    Y_hat = [round(yhat) for yhat in model.predict(X_test)]
    score = accuracy_score(Y, Y_hat)

    return score

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8123)
