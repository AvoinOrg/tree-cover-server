import os

from flask import render_template, session, redirect, url_for, flash, current_app

from . import main
from .forms import FileForm
from .process_data import process_file
from werkzeug.utils import secure_filename

from flask import send_from_directory
import pandas as pd
from flask import request

@main.route("/", methods=["GET", "POST"])  # or e.g. /upload if want other home page
def index():
    form = FileForm()
    choice = form.choice.data
    
    if form.validate_on_submit():
        session["data"] = dict()
        f = form.file.data
        try:
            session["file_name"] = secure_filename(f.filename)
            f_path = os.path.join("files", session["file_name"])
            f.save(f_path)  # todo: current_app.instance_path, ... instead
            
            #creates a processed file in "files"
            d = process_file(f_path, choice)
            dpath = os.path.join("files","results_" +session["file_name"])
            d.to_csv(dpath)

            dan = str(len(d[d['class'] == 'danger']))
            inf = str(len(d[d['class'] == 'info']))
            war = str(len(d[d['class'] == 'warning']))
            suc = str(len(d[d['class'] == 'success']))
            
            return render_template("result_list.html", file_name=session.get("file_name"), data=d, dang=dan, info=inf, warn=war, succ=suc)
        except Exception as e:
            flash("Error during upload")
            raise e
            # return redirect(url_for('.index'))
    return render_template("index.html", form=form, file_name=session.get("file_name"))  # upload.html


#download function retrieves processed file from "files" and downloads it in Downloads
@main.route("/get-csv/<csv_id>")
def get_csv(csv_id):
    csv_name = "results_"+csv_id
    csv = os.path.abspath("files")

    # print(csv_name)
    try:
        
        return send_from_directory(csv, filename=csv_name, as_attachment=True)
    
    except Exception as e:
            flash("Error during download")
            raise e
  

#divides results based on difference
@main.route("/<disc>/<file_n>")
def see_only(file_n, disc):

    csv_name = "results_" + file_n
    csv = os.path.abspath("files")
    f_path = os.path.join("files", csv_name)

    df = pd.read_csv(f_path, engine='python')
    df = df.drop('Unnamed: 0', axis=1)
    df = df.round(7)
    
    dan = str(len(df[df['class'] == 'danger']))
    inf = str(len(df[df['class'] == 'info']))
    war = str(len(df[df['class'] == 'warning']))
    suc = str(len(df[df['class'] == 'success']))
    com = str(len(df))
    
    if (disc == "complete"): 
        return render_template("result_list.html", file_name=file_n, data=df, dang=dan, info=inf, warn=war, succ=suc)


    df = df[df['class'] == disc]


    return render_template("partial_result_list.html", file_name=file_n, data=df, discrep=disc, comp=com, dang=dan, info=inf, warn=war, succ=suc)



#downloads only partial results
@main.route("/<disc>/<file_n>/down")
def download_only(file_n, disc):

    csv_name = "results_" + file_n
    csv = os.path.abspath("files")
    f_path = os.path.join("files", csv_name)

    df = pd.read_csv(f_path, engine='python')
    df = df.drop('Unnamed: 0', axis=1)
    df = df.round(7)
    df = df[df['class'] == disc]

    csv_n = disc +"_"+ file_n

    dpath = os.path.join("files",csv_n)
    df.to_csv(dpath)

    return send_from_directory(csv, filename=csv_n, as_attachment=True)
