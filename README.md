# Wikimedia Stream App

## Purpose:
This repo aims to create a simple data stream pipeline with Python (and other things), including getting data streams from Wikimedia [Recent Changes API](https://wikitech.wikimedia.org/wiki/Event_Platform/EventStreams), processing it, persisting and presenting in a Dashboard.

To acomplish this, the following tasks were executed:

### Task 1: Planning

#### Design Considerations
- The application follows the simplest way to complete tasks, considering the time given to finish.
- In order to get data from API, the SSEClient were used as the Wikimedia Recent Changes documentation suggests. 
- Elasticsearch were used due to the nature of the data. This kind of streams can be considered as events that generates documents (json), which is a natural data to Elasticsearch.  It is scable, very fast with full text search in documents and very good to analytics workloads. MongoDB would be a candidate to store this json documents, but manage mongoDB clusters is not so easy, at least, considering what I've heard :)
- In the backend a flask server interact with Elasticsearch querying data requested from dashboard.
- DataViz were produced with standard web tools using material design, which I personally appreciate.
- A docker compose file construct environment with flask and elasticsearch.

#### Strength's and Weaknesses
- Storage is scalable in Elasticsearch cluster
- Dashboard has little self-service features, as creation of new charts. ELK stack also were provided to give more self-service capabilities. - Just one python process to deal with all messages could cause event loss. Some fastdata tool could be used instead, as flume, spark streaming, even kafka.

#### Pipeline

![Pipeline](./doc/assets/img/pipeline.png)


### Task 2: Getting data

Initially data were collect from Wikimedia Recent Changes API through a python application (wikimedia_app).
This application uses the service Consumer which collect streams of messages from API and then write these data to some user option (console, json file or persist them into Elasticsearch) - Task 3. 

Diagram:

![Task2](./doc/assets/img/task2.png)

The user select the output desired based on app arguments are passed in.
Application's command line help:

```shell
/path/to/project/wikimedia_stream/app$ python wikimedia_app.py -h
usage: Wikimedia Stream Consumer [-h] --mode {console,file,persist}
                                 [-f FILTER] [-o OUTPUT]

Simple wikimedia stream consumer

optional arguments:
  -h, --help            show this help message and exit
  --mode {console,file,persist}
                        Output mode. Default is console, which prints messages
                        to sysout. When file is desired it is necessary to
                        pass output path to file. Persist mode will write
                        events to Elasticsearch.
  -f FILTER, --filter FILTER
                        Filter to be executed on Wikimedia EventStream data
                        based on regex. The regex pattern will be searched in
                        all message, including all fields
  -o OUTPUT, --output OUTPUT
                        Path to output file
```


### Task 3: Persist data

- Verify Elasticsearch instance

``` shell
curl -X GET localhost:9200/
{
  "name" : "aaf67203e99f",
  "cluster_name" : "docker-cluster",
  "cluster_uuid" : "ex3iSq5uQDW1qmq20Tvvvg",
  "version" : {
    "number" : "7.1.0",
    "build_flavor" : "default",
    "build_type" : "docker",
    "build_hash" : "606a173",
    "build_date" : "2019-05-16T00:43:15.323135Z",
    "build_snapshot" : false,
    "lucene_version" : "8.0.0",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}
```
- Creating index

``` python
    python initdb.py
```

- Persist stream

``` python
python wikimedia_app.py --mode=persist
```
- See data persisted

``` shell
curl -H 'Content-Type: application/json' -XGET localhost:9200/dasa/_search?pretty
```

Postman:
![Postman](./doc/assets/img/postman.png)

### Task 4: DataViz

Two options were given to data visualization and ad-hoc queries:

- *1: Simple HTML dashboard with charts required.*
  - [AdminBSBMaterialDesign](https://github.com/gurayyarar/AdminBSBMaterialDesign)
  - [Material Design](https://design.google/)
  - Flask application

- *2: ELK Stack* 
  - [ELK stack (Elasticsearch, Logstash, Kibana)](https://github.com/deviantony/docker-elk)

### Task 5: Query reporting

Skipped. Kibana provide this feature.

### Task 6: Docker

An image with the applcation were composed with ELK image, in order to integrate them. Follow instructions below to run entire application.

## Running Application

Firstly, clone the project to your machine:

``` shell
git clone https://github.com/amommendes/wikimedia_stream.git
```
Configure virtualenv and install dependencies 

``` shell
virtualenv -p /usr/bin/python3.6 venv
pip install -r requirements.txt
source venv/bin/activate
```

Below, I described steps to run every task:

- *Task 2:*

Prerequisites:
- Python 3.6
- pip
-virtualenv

- See command-line help
``` shell
  python app/wikimedia_app.py -h
  usage: Wikimedia Stream Consumer [-h] --mode {console,file,persist}
                                 [-f FILTER] [-o OUTPUT]

  Simple wikimedia stream consumer

  optional arguments:
  -h, --help            show this help message and exit
  --mode {console,file,persist}
                        Output mode. Default is console, which prints messages
                        to sysout. When file is desired it is necessary to
                        pass output path to file. Persist mode will write
                        events to Elasticsearch.
  -f FILTER, --filter FILTER
                        Filter to be executed on Wikimedia EventStream data
                        based on regex. The regex pattern will be searched in
                        all message, including all fields
  -o OUTPUT, --output OUTPUT
                        Path to output file
2019-06-02 05:34:11,019: Wikimedia-StreamApp : [INFO] Bye, bye
```
- See results in the console

``` shell
python app/wikimedia_app.py --mode=console
2019-06-02 05:35:30,103: Wikimedia-StreamApp : [INFO] Starting Wikimedia Streams App
2019-06-02 05:35:30,258: Wikimedia-StreamApp : [INFO] Namespace(filter=None, mode='console', output=None)
/home/amom/projects/dasa/wikimedia_stream/app/config/environment.py:13: YAMLLoadWarning: calling yaml.load() without Loader=... is deprecated, as the default Loader is unsafe. Please read https://msg.pyyaml.org/load for full details.
  config = load(cfg)
2019-06-02 05:35:30,284: Wikimedia-StreamApp : [INFO] Configuration file successfully loaded: {'version': 1.0, 'url': 'https://stream.wikimedia.org/v2/stream/recentchange', 'es_host': 'localhost:9200', 'es_index': 'dasa', 'es_shards': 3, 'es_replicas': 1}
2019-06-02 05:35:31,542: Wikimedia-StreamApp : [INFO] Message: 
{
    "bot": false,
    "comment": "/* wbcreateclaim-create:1| */ [[Property:P18]]: Roodlands Hospital, Haddington - geograph.org.uk - 552167.jpg, ([[:toollabs:editgroups/b/harvesttemplates/1c7406583fe4|details]])",
    "id": 991064624,
    "length": {
        "new": 3160,
        "old": 2761
    },
    "meta": {
        "domain": "www.wikidata.org",
        "dt": "2019-06-02T08:35:30Z",
        "id": "619b1c31-8511-11e9-9cfc-1418776139a6",
        "request_id": "XPOKUgpAAE4AADSebaUAAABT",
        "schema_uri": "mediawiki/recentchange/2",
        "topic": "eqiad.mediawiki.recentchange",
        "uri": "https://www.wikidata.org/wiki/Q28406015",
        "partition": 0,
        "offset": 1631577157
    },...
```

- Test a regex filter

``` shell
python app/wikimedia_app.py --mode=console --filter=".*en.wikipedia.*"
2019-06-02 05:51:51,019: Wikimedia-StreamApp : [INFO] Starting Wikimedia Streams App
2019-06-02 05:51:51,019: Wikimedia-StreamApp : [INFO] Namespace(filter='.*en.wikipedia.*', mode='console', output=None)
/home/amom/projects/dasa/wikimedia_stream/app/config/environment.py:13: YAMLLoadWarning: calling yaml.load() without Loader=... is deprecated, as the default Loader is unsafe. Please read https://msg.pyyaml.org/load for full details.
  config = load(cfg)
2019-06-02 05:51:51,020: Wikimedia-StreamApp : [INFO] Configuration file successfully loaded: {'version': 1.0, 'url': 'https://stream.wikimedia.org/v2/stream/recentchange', 'es_host': 'localhost:9200', 'es_index': 'dasa', 'es_shards': 3, 'es_replicas': 1}
2019-06-02 05:51:52,540: Wikimedia-StreamApp : [INFO] Message: 
{
    "bot": false,
    "comment": "You have been indefinitely blocked from editing because your account is being used only for [[WP:SPAM|spam or advertising]] and your username is a violation of the [[WP:U|username policy]]. ([[WP:TW|TW]])",
    "id": 1159325130,
    "length": {
        "new": 5903,
        "old": 3349
    },
    "meta": {
        "domain": "en.wikipedia.org",
        "dt": "2019-06-02T08:51:51Z",
        "id": "aa53c834-8513-11e9-9f86-1866da9949ff",
        "request_id": "XPOOJwpAEMUAALaJHPAAAABC",
        "schema_uri": "mediawiki/recentchange/2",
        "topic": "eqiad.mediawiki.recentchange",
        "uri": "https://en.wikipedia.org/wiki/User_talk:Beautyakwinder",
        "partition": 0,
        "offset": 1631601605
    },

```

- Write results to a file 

``` shell

python app/wikimedia_app.py --mode=file --output=message.json

```

- *Task 3:*

Prerequisites:
- Docker
- Docker-compose

Build and run ELK stack with docker-compose (this can take a long time).

``` shell
# from project root directory
sh build.sh
```

After container are up and run, execute initdb.py, which will create the "dasa" index in Elastisearch. This step is not strictly necessary, since that Elasticsearch will create the index when messages are sent.

``` shell
# Go to project root directory
python app/db/initdb.py
```

Write client to write data into Elasticsearch

``` shell
python wikimedia_app.py --mode=persist
```

The results can be observed as described in [Task 3](#task-3-persist-data).

- *Task 4:*

Prerequisites:
- ELK and Dashboard stack up and running (See Task 3).
- Virtualenv

- 1 - Dashboard:

  - Start Flask App
  ``` shell
  cd app
  export FLASK_APP=dashboard
  export FLASK_ENV=development
  flask run 
  ```
  *Note: if you are running dashboard indepently from docker, you need to change the es_host property inside app/config/app_config.yml to localhost:9200*

  - Go to browser: localhost:5001

  - 2 - Kibana

  With ELK stack up and running, go to browser: localhost:5601.






