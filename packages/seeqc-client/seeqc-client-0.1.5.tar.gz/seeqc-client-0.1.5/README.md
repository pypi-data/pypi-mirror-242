
## SEEQC CLI User Guide

Seeqc CLI is a library for interfacing with SEEQC's quantum devices via the cloud.

### Prerequisite
SEEQC CLI requires an installation of Python>=3.8 along with Pip. We suggest installing SEEQC CLI into a new virtual environment.
Using SEEQC CLI will require a username and password which can be obtained by request.

### Installation
The library should be installed from PyPi using Pip as:
````
 pip install seeqc-client
 ````
This will install SEEQC CLI into your active Python environment along with its dependencies.
### Getting Started
Instantiate the client as:

````
from seeqc_client import Client

client = Client()

client.initialise()
````
This will prompt username and password entry and upon success provide the client with the credentials required to access our systems. The client will require re-instantiation once per day.
### Running Experiments
Experiments can be created using QASM format files **ADD THE VALID GATE LIST** as:
````
exp = client.create_experiment('./my_experiment.qasm')
````
This will create a new experiment object associated with this QASM file that can be submitted to be run as:
````
exp.run()
````
This sends the QASM instructions to our platform and returns an experiment id which can be used to recover experiments from another session.
The status of the experiment can be checked as:
````
exp.get_status()
````
The status will iterate through pending, running and complete. Once the status is set to complete it will automatically retrieve the experiment results, which can then be viewed as:
````
exp.show_results()
````
Results here correspond to the population distributions. To return the full quantum register as a numpy array instead use
````
exp.get_register()
````
### Retrieving Experiments
Metadata on previous experiments can be accessed as:
````
client.get_experiments(start_index, end_index)
````
If no indices are provided the last 10 experiments you ran will be returned.
From the list of experiments you can retrieve the experiment id which can be used to reload a previous experiment as:
````
exp = client.get_experiment(experiment_id)
````
checking the status as shown above will recover the associated data providing the experiment has completed.

### Plotting
To produce a histogram of results distributions:
````
exp.plot()
````

### Running the emulator
The emulator accepts QASM files and the result is returned in the same function call that made the request.
The result format is a list of results per shot.
````
results = client.run_emulator('./my_experiment.qasm')
````
