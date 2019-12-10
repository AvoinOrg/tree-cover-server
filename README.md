## Installation

```bash
git clone --recurse-submodules https://github.com/LyteFM/tree-cover-server.git
virtualenv --python=python3.7 venv
source venv/bin/activate
pip install -r requirements.txt
```

Compile the sqlite extension file into the tree cover directory. Instructions are given for Linux, for other OS check the `extension-functions.c`.
``` bash
cd treecover
gcc -fPIC -lm -shared extension-functions.c -o libsqlitefunctions.so
cd ..
```

#### launch server
For local development in debug mode, run:
```bash
export FLASK_APP=server.py
export FLASK_DEBUG=1
flask run
```

For production use, you can use:
```bask
gunicorn wsgi:app
```

If you get an import error for `flask_bootstrap`, try `deactivate` and `source venv/bin/activate` again. Ensure that you're
authenticated via `earthengine authenticate`. You can use the UI in two ways:
1. Upload a _small_ CSV file with the columns `longitude`, `latitude`, `Aridity_Zone` and optionally a `plot_id`. An example is given in `treecover/data/example_fetch_sentinel_input.csv`.
2. Upload a CSV with already populated features by using the command line tool. Example: `treecover/data/example_server_sentinel_input.csv` or `example_input_file_landsat.csv`

The webapp without working GEE retrieval can be viewed at: http://tree-cover.herokuapp.com/
In order to use the submodule, [this buildback](https://elements.heroku.com/buildpacks/timvanmourik/heroku-buildpack-git-submodule) is used: 




#### command line tool for data retrieval
The command line tool located in `treecover/sentinel.py` can be used to fetch raw data for the locations given in a CSV file with columns `longitude`, `latitude`, `Aridity_Zone` and optionally a `plot_id`.
If the compiled extension is not located in `treecover/libsqlitefunctions.so`, you need to pass its location as `--libsqlite PATH/TO/EXTENSION` for modes 1 and 3.
You can use it in the following modes:
1. Only write the necessary features to a specified csv file
2. Only write the raw fetched data to a sqlite db
3. Write the raw fetched data to a sqlite db and export the features to a csv file

```bash
source venv/bin/activate
cd treecover
# Mode 1:
python3 sentinel.py data/example_fetch_sentinel_input.csv --output outfile_1.csv
# Mode 2:
python3 sentinel.py data/example_fetch_sentinel_input.csv --db data/my_small_test.db
# Mode 3:
python3 sentinel.py data/example_fetch_sentinel_input.csv --db data/my_small_test.db --output my_small_outfile.csv
```

In order to save some RAM, you can specify e.g. `--chunk 10` in order to commit transactions/ append to the csv after 10 instead of the default of 100 processed rows.
Then, a GCP f1-micro with enough disk space is sufficient.

