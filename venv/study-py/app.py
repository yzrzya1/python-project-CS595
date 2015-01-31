
from flask import Flask
from flask import render_template

app = Flask(__name__)
@app.route("/")
def index():
        username = "zhang"
        head = "Starting"
        name=[{'username':'zhang','age':'18'},{'username':'wang','age':'19'}]
        return render_template("index.html",name=username,head=head,listdata=name)


if __name__=="__main__":
        app.run(debug=True)
