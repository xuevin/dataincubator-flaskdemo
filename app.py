from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/stock')
def stock():
   nquestions=5
   return render_template('stock.html',num=nquestions)

if __name__ == '__main__':
  app.run(port=33507)
