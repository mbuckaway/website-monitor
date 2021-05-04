# Website Monitor

This is a simple website monitor. It connects to a website, records the amount of time for a connection, if the connection is successful or not, sends the data to Apache Kafka and stores the data in a Postgres DB for later retrieval. Both Kafka and Postgres are hosted at Aiven. This code does not implement the front end code to show the data but could easily be connect to Grafana as the front end. Similarly, the design could be re-implemented using AWS MQ and Aurora DB running the producers and consumer threads in different containers. Aiven just makes using the open source version easy.

This is a test app to experiment with Kafka and PostgreSQL hosted at Aiven and nothing more.

## Design details

This is a simple system that monitors single website availability over the network, produces metrics about this website and passes these events through an Aiven Kafka instance into an Aiven PostgreSQL database.

A Kafka producer which periodically checks the target websites and sends the check results to a Kafka topic, and a Kafka consumer storing the data to an Aiven PostgreSQL database. For testing purposes, these components may run in the same machine, but in production use similar components would run in different systems. The application is packaged using setuptools. While a Dockerfile is provided, it is not complete.

The website checker performs checks periodically and collect the HTTP response time. The code checks the response code and stores a success/false flag with the response time data. If this were a "real" system, we would also store the response code and provide a way to check the returned webpage for a regex or similar to make sure the data is valid. The status code is not stored and website regex has not been implemented.

For the database writer, the solution that records the check results into one or more database tables and could handle a reasonable amount of checks performed over a longer period of time. The current DB code writes data to the datbase, but makes no check to validate the data. For a production system, this test would be implemented. Further, since metrics are returned and stored, a time series database would have been a better choice (for excample, the TimeSeriesDB plugin to PostresSQL)

For simplicity, the tests assume PostgreSQL and Kafka are already running in the Aiven cloud. The .env file defines the hostnames and configuration. Cert files are expected to be downloaded and stored, by default, in the certs directory. The path to the Kafka cert files is defined in the .env file. The connection to PostrgeSQL is not encrypted, and should be. However, there is no requirement from Aiven to have an encrypted connection (or works unencrypted without specifying a cert).

This test program uses Aiven as a Database as a Service vendor. If you want to try them, please register to Aiven at https://console.aiven.io/signup.html at which point you'll automatically be given $300 worth of credits to play around with. The credits should be enough for a few hours of use of their services.

There is no ORM in use here, although, SQLAlchamy would have made life easer. Also missing is a finished Dockerfile and a way to configure the settings though Docker. The webmoncheck script also only handles one URL at a time, and could have handled a list of the them, or had this information added to the config file or had it reside in the database. Lots of options here, but the initial requirements didn't indicate more than one website was required to be checked.

## Testing

This code was developed using Visual Studio Code on MacOS. For the postgresql python driver to be able to be installed on MacOS, one must first install PostgreSQL to get access to the client libraries which are required for the psycopg2 package to be installed. This can be done with Brew:

```bash
brew install postgresql
```

Once testing has been completed and/or the code moved into a container, postgresql can be removed.

Similarly, client libraries would need to be installed on Linux if Linux is used.

## Installation

This code was tested on Python 3.9 and will require at least Python 3.6 to run as it makes use of type hints.

To get the code running.

1. Checkout the code.
2. Copy .env.sample to .env and edit to match your settings
3. Create a virtual env for testing:

```
python3 -m venv env
```

4. Activate the virtual env:

```
. env/bin/activate
```

5. Download the Kafka certs and put them in the certs directory. You can put them anywhere, but the default setup assumes this directory.  Make sure the .env file matches the cert location and names.
6. Run:

```
python3 setup.py install
```

This will install the utility.

7. Run the producer:

```
webmoncheck -u http://www.website.com
```

This assumes the .env is in the current directory. If it is not, use the -e command line option to specify it. Keep in mind, you cannot have a .env in the current directory and specify the -e option at the same time. The .env in the current directory will take precidence.

8. In another shell prompt, run the consumer:

```
webmonsave
```

Again, this assumes the .env is in the current directory. If it is not, use the -e command line option to specify it. Keep in mind, you cannot have a .env in the current directory and specify the -e option at the same time. The .env in the current directory will take precidence.

## The Config

The configuration uses the dotenv package to manage the config. This means the same contents of the .env can be specified in the environment before running the programs. This makes it convenient to use in a Docker container where the environment variables can be used to configure the programs.

The following environment/.env variables are used:

| Env Variable | Use |
|--------------|-----|
| DATABASE_HOST | PostgresSQL Database hostname |
| DATABASE_PORT | Database port |
| DATABASE_DB | Name of the database to use |
| DATABASE_USER | Database user |
| DATABASE_PASSWD | Database user password |
| KAFKA_HOST | Url for Kafka (include port number if non-standard) |
| KAFKA_TOPIC | Kafka topic to use |
| KAFKA_USER | Kafka user |
| KAFKA_CAFILE | Kafka ca.pem filename |
| KAFKA_CERTFILE | Kafka cert filename (ie. service.cert) |
| KAFKA_KEYFILE | Kafka private key filename (ie. service.key) |

### References

[Getting started with Apache Kafka in Python](https://towardsdatascience.com/getting-started-with-apache-kafka-in-python-604b3250aa05)
[How to measure Service Response time in Python](https://stackoverflow.com/questions/43252542/how-to-measure-server-response-time-for-python-requests-post-request#43260678)