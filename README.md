# Demo: Rocketry with FastAPI

This is a demo for creating a scheduler with an API.
We use [Rocketry](https://rocketry.readthedocs.io/)
for our scheduler and [FastAPI](https://fastapi.tiangolo.com/)
for our API.

This contains three source files:

- ``app/api.py``: FastAPI application
- ``app/scheduler.py``: Rocketry application
- ``app/main.py``: Main launch script

Add your tasks need to ``app/scheduler.py`` and 
modify ``app/api.py`` as needed.

## Installation

Clone this repository:

```console
git clone https://github.com/Miksus/rocketry-with-fastapi.git
```

Make sure you have Python 3.7 or newer.
Then just install the dependencies:

```console
pip install -r requirements.txt
```

## Running

```console
python app/main.py
```

## What next?

Read more about Rocketry:

- Documentation: https://rocketry.readthedocs.io/
- Source code: https://github.com/Miksus/rocketry

Read more about FastAPI:

- Documentation: https://fastapi.tiangolo.com/
- Source code: https://github.com/tiangolo/fastapi