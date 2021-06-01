
from flask import Flask, render_template, request, redirect, url_for, session

from transpose import dframe

app = Flask(__name__)
app.config["DEBUG"] = True


comments = []
keys  = []
kms = []

@app.route('/chords', methods=["GET", "POST"])
def wibble():
    return redirect(url_for('.index'))

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "GET":
        if len(comments) < 1:
            return render_template("chords.html")
        else:
            output = comments.pop()
            kee = keys.pop()
            kee = 'Possible keys: ' + str(kee)
            km = kms.pop()
            return render_template("chords.html", comments=comments, op = output, key_message = km,  key = kee)


    output = request.form["contents"]

    stp = int(request.form["steps"])
    print(stp)

    try:
        lizt = output.split('\n')
        transposed, km, kee = dframe(lizt, stp)

        comments.append(transposed)
        keys.append(kee)
        kms.append(km)
    except:
        comments.append("no chords detected, please try again")
        keys.append('')
        kms.append('')
    return redirect(url_for('.index'))

    session.clear()