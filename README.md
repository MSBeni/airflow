# Airflow README

## installation
First create a virtual environment and name it whatever you want.
Then activate the environment and run this command on your terminal to install airflow on your system. (I assume you are working on ubuntu which is pretty normal)
```bash
pip3 install apache-airflow==2.0.0 --constraint https://gist.githubusercontent.com/marclamberti/742efaef5b2d94f44666b0aec020be7c/raw/5da51f9fe99266562723fdfb3e11d3b6ac727711/constraint.txt
```
run this command for airflow matastore initialization and also creating files and folders needed by airflow. We just use this comamnd once.
```bash
airflow db init
```
Now if you check your system list using ```ls``` you will have a folder named airflow and you can check
it simply by typing ```cd airflow/```.

To run the airflow webserver just type this command on your terminal:
```bash
airflow webserver
```
If now you check your localhost at port 8080, you will be in the interface admin page.
Now to create a user to login to the admin page, you can use this command:
```bash
airflow users create -u admin -p admin -f MS -l Beni -r Admin -e admin@airflow.com
```
Now you have a user with username and password admin which has an Admin ROLE.
Note: By typing the help method you can find a good guidance how to do it:
```bash
airflow users create -h
```
you will this such result:
```
usage: airflow users create [-h] -e EMAIL -f FIRSTNAME -l LASTNAME
                            [-p PASSWORD] -r ROLE [--use-random-password] -u
                            USERNAME

Create a user

optional arguments:
  -h, --help            show this help message and exit
  -e EMAIL, --email EMAIL
                        Email of the user
  -f FIRSTNAME, --firstname FIRSTNAME
                        First name of the user
  -l LASTNAME, --lastname LASTNAME
                        Last name of the user
  -p PASSWORD, --password PASSWORD
                        Password of the user, required to create a user without --use-random-password
  -r ROLE, --role ROLE  Role of the user. Existing roles include Admin, User, Op, Viewer, and Public
  --use-random-password
                        Do not prompt for password. Use random string instead. Required to create a user without --password 
  -u USERNAME, --username USERNAME
                        Username of the user

examples:
To create an user with "Admin" role and username equals to "admin", run:

    $ airflow users create \
          --username admin \
          --firstname FIRST_NAME \
          --lastname LAST_NAME \
          --role Admin \
          --email admin@example.org

```
Then please run the command below to run the scheduler:
```bash
airflow scheduler
```

## Other useful commands:
- Start the Scheduler
```bash
airflow scheduler
```
- Start a Worker Node If you are in distributed mode (Celery)
```bash
airflow worker
```

- Print the List of Active DAGs
```bash
airflow list_dags
```
You can use ```airflow tasks list name_of_dag``` to check that every thing is good with your data pipeline. it should show all the necessary tasks.

- Print the List of Tasks of the dag_id
```bash
airflow list_tasks dag_id
```
Exemple:
```bash
airflow list_tasks hello_world
```

- Print the Hierarchy of Tasks in the dag_id
```bash
airflow list_tasks dag_id --tree
```
Exemple:
```bash
airflow list_tasks hello_world --tree
```

- Test your Tasks in your DAG
```bash
airflow test dag_id task_id execution_date
```
Exemple:
```bash
airflow test hello_world hello_task 2018-10-05
```


## Test the tasks
You can test each implemented task, immediate after setup using this command:
```bash
airflow tasks test dag_id task_id start_date 
```
for example, you can test the creating_table task like this:
```bash
airflow tasks test user_processing creating_table 2020-01-01
```
or in testing new task:
```bash
airflow tasks test user_processing is_api_available 2020-01-01
```

## Checking the Available Sqlite Tables
Write this command and then you can have have access to the sqlite and can check the available tables:
```bash
sqlite3 airflow.db
```
Then type command ```.tabels``` to see the available tables:
```bash
sqlite> .tabels
```


## Configuring Executor in Airflow
Two parameters are used in airflow in order to configure your executor.
- 1- sql_alchemy_conn
- 2- executor

for the sql_alchemy_conn run this command in the corresponding airflow virtual environment:
```bash
airflow config get-value core sql_alchemy_conn
```
You should receive such an output: sqlite:////home/i-sip_iot/airflow/airflow.db

for the executor run this command in the corresponding airflow virtual environment:
```bash
airflow config get-value core executor
```
You should receive such an output: SequentialExecutor



## Configuring Postgresql in Airflow
First enter the installed postgresql service in your terminal by typing:
```bash
sudo -u postgres psql
```

If you do not have still a postgresql service installed on your system, please find the link below:
Please consider this important note that you should be able to connect to your postgresql. Use the guidance here: https://github.com/MSBeni/SmartContactTracing_Chained/blob/master/chainedSCT/extraction/README.md

After that use command: 
```bash
ALTER USER postgres PASSWORD 'postgres';
```
You will receive a message ```ALTER ROLE```, hit ```ctrl+d``` to jump out of the postgres console.

Now install an extra package for the postgres:

```bash
pip install 'apache-airflow[postgres]'
```
Now you should configure the postgres. Open the file ```airflow.cfg``` and change and set these values:
```
sql_alchemy_conn = postgresql+psycopg2://postgres:postgres@localhost/postgres
```
and 
```
executor = LocalExecutor
```

You can check the new setting by writing this smple command in terminal:
```bash
airflow db check
```
You should receive "connection successful" message.

By using the LocalExecutor we can run multiple tasks in parallel.

Now you should initialize the DB again, so simply type the coammand below as stated before:
```bash
airflow db init
```
Now create an airflow user with this command:

```bash
airflow users create -u admin -p admin -f admin -l admin -r Admin -e admin@airflow.com
```
You will receive the message: "Admin user admin created"

Now we are ready to run airflow:
```bash
airflow webserver
```
and then:
```bash
airflow scheduler
```


## Celery Executor
CeleryExecutor is one of the ways you can scale out the number of workers. For this to work, you need to setup a Celery backend (RabbitMQ, Redis, …) and change your airflow.cfg to point the executor parameter to CeleryExecutor and provide the related Celery settings.
Please find this link in order to find the complete guidance: "https://airflow.apache.org/docs/apache-airflow/stable/executor/celery.html"

Please note that you must have the flower python library already installed on your system. The recommended way is to install the airflow celery bundle.
```bash
pip install 'apache-airflow[celery]'
```

We also need to have the redis installed on our system:
```bash
sudo apt update
```
```bash
sudo apt install redis-server
```

so now we need to change the redis configuration file to be ready to used in airflow:
```bash
sudo nano /etc/redis/redis.conf
```

then change the value supervosed form no to systemd:
```
supervised systemd
```
Then press: ```ctrl+d, y, enter```

Now we are done, restart the systemctl redis with this command:
```bash
sudo systemctl restart redis.service
```
Now check the status of the redis:
```bash
sudo systemctl status redis.service
```

Now open the airflow.cfg and then change the executor from "LocalExecutor" to "CeleryExecutor"

We also need to change the broker_url which used by redis to push the task to the redis message broker, so we ned to specify the connection corresponding to the redis instance  
```bash
broker_url = redis://localhost:6379/0
```
We also should change the "result_backend":
```bash
result_backend = postgresql+psycopg2://postgres:postgres@localhost/postgres
```

a connection same as sqlalchemy.

