## Installation

```bash
git clone https://github.com/LyteFM/tree-cover-server.git
--recurse-submodules
virtualenv --python=python3.7 venv
source venv/bin/activate
pip install -r requirements.txt
```

#### launch server

```bash
export FLASK_APP=server.py
export FLASK_DEBUG=1
flask run
```

If you get an import error for `flask_bootstrap`, try `deactivate` and `source venv/bin/activate` again.

#### fetching updates

This includes also the updates from the analysis part `tree-cover`.

```bash
git pull --recurse-submodules && git submodule update
```
