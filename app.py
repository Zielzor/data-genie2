from flask import Flask, render_template, request, make_response
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        global df, column_names
        df = pd.read_csv(file)
        column_names = df.columns.tolist()
        return render_template('index.html', column_names=column_names, data_loaded=True)
    return render_template('index.html', error='No file selected.')

@app.route('/filter', methods=['POST'])
def filter_data():
    selected_columns = request.form.getlist('columns')
    filtered_df = df[selected_columns]
    for column in selected_columns:
        checkbox_values = request.form.getlist(column)
        if checkbox_values:
            filtered_df = filtered_df[filtered_df[column].isin(checkbox_values)]
    return render_template('index.html', column_names=column_names, filtered_df=filtered_df, data_loaded=True)

@app.route('/export', methods=['POST'])
def export_data():
    data = request.form['data']
    response = make_response(data)
    response.headers['Content-Disposition'] = 'attachment; filename=filtered_data.csv'
    response.headers['Content-type'] = 'text/csv'
    return response

@app.route('/statistics', methods=['POST'])
def calculate_statistics():
    statistics = df.describe().to_html()
    return render_template('index.html', column_names=column_names, statistics=statistics, data_loaded=True)

if __name__ == '__main__':
    app.run(debug=True)