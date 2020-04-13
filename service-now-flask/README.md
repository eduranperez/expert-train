# Slack Bot

This Flask application will receive POST requests from Slack and perform the appropriate business logic to provide an interface between Slack and Service Now.

## Getting Started

The project lives within the `service-now-flask` directory.

### Prerequisites

* Python 3.7 installation
* pipenv that supports python 3 and that has access to pypi.org for packages

To run the Slack Bot API, make sure you have the latest version via the repository on Github @ https://github.com/eduranperez/expert-train.

### Installing

Install the pip dependencies via 

```
expert-train/service-now-flask $ pipenv install 
```

To run the Slack Bot API for development and testing, you have to install the development dependencies with the extra `-d` flags for `pipenv install`

```
expert-train/service-now-flask $ pipenv install -d
```

To run the flask app, change directory to `expert-train/service-now-flask`

Create a .env file with the below config.

```
FLASK_ENV=development
FLASK_APP='src/service_now_proxy/app.py:create_app()'
SN_USERNAME='Your service now username'
SN_PASSWORD='Your service now password'
SN_INSTANCE_URL='Your service now instance'
```
Then run the app with 

```
pipenv run flask run --host=0.0.0.0 --port=5000 --debugger
```

### Updating The Documentation

In order to update the sphinx html documents, you have to have the development dependencies installed.

In the expert-train/service-now-flask/docs directory run the below

```
expert-train/service-now-flask/docs $ pipenv run make html
```

The raw html files will then live in the expert-train/service-now-flask/docs/build/html

To create a new page add a reference to it under "Contents" in index.rst.  For example to add an "Endpoints" page 

```
.. toctree::
   :maxdepth: 2
   :caption: Contents:

   flowdiagram
   endpoints
```

Then create a new rst file with the same name in the directory
```
expert-train/service-now-flask/docs/source
```

Continuing the example.

```
  endpoints.rst
```

Place all page content inside this file and run the make command again to see your changes.  

To add a new flow diagram it is recommended to first build the diagram using a live editor such as https://mermaid-js.github.io/mermaid-live-editor

The just paste the resulting mermaid code into one of your rst pages.  For example with the endpoints page we might have.

```
Slack Bot's Incident Endpoint Flow Diagram
=====================================

.. mermaid::

  graph TD;
    A(/GetIncidentDetails) --> B(Fetch Incident details)
```
For more information about mermaid syntax please visit their page at https://mermaid-js.github.io/mermaid/#/n00b-syntaxReference

To view your pages open any of the resulting html files inside of
```
expert-train/service-now-flask/docs/build/html
```
with the browser of your choice.

## Versioning

We use [SemVer](http://semver.org/) for versioning.

## Authors

* **Edgar Perez** [eduranperez](https://github.com/eduranperez/)
