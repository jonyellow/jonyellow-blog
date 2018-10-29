from flask import Flask, render_template

app = Flask(__name__)


class Person():
    def __init__(self,n,a,s):
        self.name = n
        self.age = a
        self.score = s

p = Person('hao', 23, 67)

l = [1,2,3,4,5]

@app.route('/')
def index():
    return render_template('index.html',params = l)

@app.route('/login')
def login():
    return "<h3>hello</h3>"

if __name__ == '__main__':
    app.run(DEBUG=True)
