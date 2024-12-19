from flask import Flask, render_template, send_file

app = Flask(__name__)

# Route to serve the HTML file
@app.route("/")
def index():
    return render_template("index.html")

# Route to serve the JSON file
@app.route("/data")
def data():
    return send_file("SofaData.json", mimetype="application/json")

@app.route("/index.js")
def indexjs():
    return send_file("index.js", mimetype="application/js")

@app.route("/sort.js")
def sortjs():
    return send_file("sort.js", mimetype="application/js")

@app.route("/slideshow.js")
def slideshowjs():
    return send_file("slideshow.js", mimetype="application/js")

@app.route("/styles.css")
def styles():
    return send_file("styles.css", mimetype="text/css")

if __name__ == "__main__":
    app.run(debug=True)
