from flask import Flask, render_template ,redirect, url_for,request,jsonify,session
import json
import copy
import csv
import sys
import matplotlib
matplotlib.use('Agg')

import pandas
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt

df = pandas.read_csv("data.csv")

features = df.columns[:-1].tolist()

X = df[features]
y = df['Res']

dtree = DecisionTreeClassifier()
dtree = dtree.fit(X, y)

tree.plot_tree(dtree, feature_names=features)
new_data = {k:0 for k in features}
some=[]


app = Flask(__name__)
app.secret_key = 'your_secret_key' 

@app.route('/')
def home():
    return render_template('index1.html')

@app.route('/second_page')
def second_page():
    return render_template('p2.html')

@app.route('/navigate_to_second_page')
def navigate_to_second_page():
    return redirect(url_for('second_page'))

@app.route('/selected-dishes', methods=['GET'])
def handle_selected_dishes():
    selected_dishes_json = request.args.get('selectedDishes[]')
    selected_dishes = json.loads(selected_dishes_json)
    for i in selected_dishes:
        new_data[i["name"]]+=int(i["quantity"])
    dishImageMapping = {
        'Bread Barrel': 'bread-barrel.jpg',
        'Butterscotch Blast': 'cake.jpg',
        'Caesar': 'caesar.jpg',
        'Tuscan Grilled': 'tuscan-grilled.jpg',
        'Mozzarella': 'mozzarella.jpg',
        'Greek Salad': 'greek-salad.jpg',
        'Spinach Salad': 'spinach-salad.jpg',
        'Lobster Roll': 'lobster-roll.jpg',
        'Lobster Bisque': 'lobster-bisque.jpg',
    }


    return render_template('ex.html', selected_dishes=selected_dishes, dishImageMapping=dishImageMapping)

@app.route('/process_input', methods=['POST'])
def process_input():
    data = request.get_json()
    n = data.get('noOfPeople')
    t=0
    session['temp'] = copy.deepcopy(new_data)
    print(new_data)
    for k,v in new_data.items():
        session['temp'][k]=v/float(n)
        t=t+v
    print(t)
    new_df = pandas.DataFrame([session['temp']], columns=features)
    p = dtree.predict(new_df)
    result = 'green' if p == "yes" else 'red'

    return jsonify({'result': result , 't': t })

@app.route('/process_feedback', methods=['POST'])
def process_feedback():
    data = request.get_json()
    feedback_option = data.get('feedback')
    print(feedback_option)
    l=[]
    temp = session.get('temp', {})
    print(temp)
    for i in features:
        l.append(temp[i])
    l.append(feedback_option)
    print(l)
    with open('data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(l)
    return jsonify({'message': 'Feedback received successfully'})

    

if __name__ == '__main__':
    app.run(debug=True)
