import os
import pandas as pd

from flask import Flask, render_template, request, redirect

from inference import get_prediction
from commons import format_class_name

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

# Solution création de l'HTML à la main
def upload_file_v1():
    if request.method == 'POST':
        if 'file' not in request.files:
            print("redirection")
            return redirect(request.url)
        files = request.files.getlist('file')
        pagehtml='<table border="1"><thead><tr><th>Nom du fichier</th><th>Prédiction</th></tr></thead><tbody>'
        for file in files:
            # print(file)
            if not file:
                return 
            img_bytes = file.read()
            class_name, class_id = get_prediction(image_bytes=img_bytes)
            print(file.filename, class_name, class_id)
            pagehtml=pagehtml+'<tr><td>'+file.filename+'</td><td>'+class_name+'</td></tr>'
        pagehtml=pagehtml+'</tbody></table>'
        return html(pagehtml)
    return render_template('index.html')

# Solution avec DataFrame to HTML
def upload_file_v2():
    if request.method == 'POST':
        if 'file' not in request.files:
            print("redirection")
            return redirect(request.url)
        files = request.files.getlist('file')
        df=pd.DataFrame(columns=['Fichier','Prédiction'])
        for file in files:
            # print(file)
            if not file:
                return 
            img_bytes = file.read()
            class_name, class_id = get_prediction(image_bytes=img_bytes)
            print(file, class_name, class_id)
            df=df.append({'Fichier' : file.filename, 'Prédiction' : class_name}, ignore_index=True)
        return html(df.to_html())
    return render_template('index.html')

def html(content):  # Also allows you to set your own <head></head> etc
    return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"><link rel="stylesheet" href="//stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css" integrity="sha384-GJzZqFGwb1QTTN6wy59ffF1BuGJpLSa9DkKMp0DgiMDm4iYMj70gZWKYbI706tWS" crossorigin="anonymous"><style>.bd-placeholder-img {font-size: 1.125rem;text-anchor: middle;}@media (min-width: 768px) {.bd-placeholder-img-lg {font-size: 3.5rem;}}</style><link rel="stylesheet" href="/static/style.css"><title>Image Prediction using PyTorch</title></head><body class="text-center"><form class="form-signin" method=post enctype=multipart/form-data><img class="mb-4" src="/static/logo.png" alt="" width="72"><h1 class="h3 mb-3 font-weight-normal">Prediction</h1> <h5 class="h5 mb-3 font-weight-normal"></h5> <p class="mt-5 mb-3 text-muted">' + content + '</p> </form> <script src="//code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script> <script src="//cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.6/umd/popper.min.js" integrity="sha384-wHAiFfRlMFy6i5SRaxvfOCifBUQy1xHdJ/yoi7FRNXMRBu5WHdZYu1hA6ZOblgut" crossorigin="anonymous"></script> <script src="//stackpath.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.min.js" integrity="sha384-B0UglyR+jN6CkvvICOB2joaf5I4l3gm9GU6Hc1og6Ls7i6U/mkkaduKaBhlAXv9k" crossorigin="anonymous"></script> </body> </html>'

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
