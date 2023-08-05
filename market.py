from flask import Flask, render_template, request, Response
from operator import itemgetter
import pandas as pd
import openpyxl
import os

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/market/')
def marketplace():
    df = pd.read_excel('Phones.xlsx')

    sort_column = request.args.get('sort_column', 'quantity')
    sort_order = request.args.get('sort_order', 'desc').lower()

    sort_order = 1 if sort_order == 'asc' else -1

    items = df.to_dict(orient='records')
    items = sorted(items, key=itemgetter(sort_column), reverse=sort_order == -1)

    resp = Response(render_template('market.html', items=items))
    resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return resp

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/huse_store')
def huse_store():
    df = pd.read_excel('Huse.xlsx')
    huse = df.to_dict(orient='records')
    huse= sorted(huse, key=itemgetter('quantity'), reverse=False)
    return render_template('huse_store.html', huse=huse)

@app.route('/incarcatoare')
def incarcatoare():
    df = pd.read_excel('Incarcatoare.xlsx')
    chargers = df.to_dict(orient='records')

    return  render_template('incarcatoare.html', incarcatoare=chargers)

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))