import os

from flask import render_template, session, redirect, url_for, flash, current_app

from . import main
from .forms import FileForm
from .process_data import process_file
from werkzeug.utils import secure_filename


@main.route("/", methods=["GET", "POST"])  # or e.g. /upload if want other home page
def index():
    form = FileForm()
    if form.validate_on_submit():
        session["data"] = dict()
        f = form.file.data
        try:
            session["file_name"] = secure_filename(f.filename)
            f_path = os.path.join("files", session["file_name"])
            f.save(f_path)  # todo: current_app.instance_path, ... instead
            flash("You have uploaded a file!")
            return render_template("result_list.html", file_name=session.get("file_name"), data=process_file(f_path))
        except Exception as e:
            flash("Error during upload")
            raise e
            # return redirect(url_for('.index'))
    return render_template("index.html", form=form, file_name=session.get("file_name"))  # upload.html
