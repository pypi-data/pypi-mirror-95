# Behavioral Signals CLI

Command Line Interface for Behavioral Signals' Emotion and Behavior Recognition in the Cloud


* Free software: MIT license
* Requires Python 3 version 3.5

Features
--------
The CLI allows you to easily:

- Submit multiple audio files to the API,
- Get behavior and emotion recognition results, call-level overview and frame-level details,
- Get speech recognition results
- Extract various features


## Installation

* Install from PyPI
```
pip3 install behavioral-signals-cli
```

* Install the most up-to-date version by cloning this repository and run

```
python3 setup.py install
```


## Getting Started

* First request your account id and token for the Behavioral Signals Web API by sending an email to api@behavioralsignals.com

* To test the service, you will need to download and extract the following set of audio and corresponding json files: [https://bitbucket.org/behavioralsignals/api-cli/downloads/data.zip]

* Change working directory to data/audio.

* Create the following configuration file, bsi-cli.conf:
```
sections:
    default:
	# The url of the web API
        apiurl: https://<WEB_API_HOST>
        # -- this apiid (aka cid) will not work -- replace it by your own token and id
        apiid: "yyyy"
        # -- this token will not work -- replace it by your own token and id
        apitoken: "xxxxx"
```

* Run the CLI to submit the test files to the API:
```
   behavioral_signals_cli --config bsi-cli.conf send_audio regression_test.csv pids.log
```
   The .csv file just contains a list of the test audio files, plus a number indicating the number of channels in the files. The pids.log file is an empty file where the process ids of the created jobs will be written.

* You can then start collecting the results:
```
   behavioral_signals_cli get_results pids.log results_dir
   behavioral_signals_cli get_results_frames pids.log results
```
   This may take some time since the CLI will keep polling for results till processing is finished. Inside the results folder you will get one .json file for each test audio file. The name of the json file will be the same as that of the corresponding audio file with the addition of a process id.

* Compare the generated json files with the ones you will find inside the results/ref folder. There could potentially be minor numerical differences but otherwise the new files should be very close to the reference ones.


Configuring the CLI
--------
The CLI requires to be properly configured in order to interact with the Behavioral Signals API.
The main variables needed to be configured are: the apiid (aka cid) a unique id provided by Behavioral Signals, apitoken (aka x-auth-token) also provided by Behavioral Signals and the apiurl, the current address of the callER service.

It allows a flexible configuration scheme by accepting with increasing priority:

-  internal defaults, apiurl: https://api.behavioralsignals.com specified in the source code of the cli
-  environment variables
-  external configuration file
-  command line opions


##### Environment variables
The CLI may be used by exporting the following as environmental variables and provide the apiurl as a command line optional parameter (see Getting Help section on how to provide the apiurl value):

- BSI_API_ID: the apiid (aka cid) provided by BSI
- BSI_API_TOKEN: the apitoken (aka x-auth-token) provided by BSI

#####  Configuration file
The CLI may be used by configuring all the required variables in a configuration file with sections,
see the configuration file of the [demo](https://bitbucket.org/behavioralsignals/api-cli/src/master/demo/).

If not specified, it will look for bsi-cli.conf in the current directory or in the home directory for the .bsi-cli.conf.

##### Command line
If the required variables are provided as command line params, see the Getting Help section how this is done, all the other configurations will be ignored.

#### Display current configuration values
  ```
  behavioral_signals_cli config  or  bsi-cli config
  ```

The output would be of the form:
```
*** bsi-cli configuration
           apiid : yyyy
        apitoken : xxxxx
          apiurl : https://api.behavioralsignals.com
  configLocation : bsi-cli.conf
      configfile : None
             log : WARNING
            stag : default
***
```


Using the Behavioral Signals CLI
--------

#### Submit audio files to the Behavioral Signals API
* Create a .csv file whose each row contains metadata for each of the audio files wish to send to the callER service. The .csv file must have the following form (order matters):
  ```
  path/to/audio/file, number of channels, call direction, agent Id, agentTeam, campaign Id, calltype, calltime, timezone, ANI, tag, meta, predictionmode, tasks
  ```

  The calltime in order to be parsed correctly should have one of the following formats:
  mm/dd/YYYY, mm-dd-YYYY, YYYY-mm-dd, dd-mm(letters)-YYYY, mm(letters)-dd-YYYY, dd/mm(letters)/YYYY, also it should be noted that timezone for the time being is ignored.

  The predictionmode property is optional and currently supports values: **audio** (Oliver only), **transcription** (ASR only), **diarization** (Diarization only), **full** (ASR + Oliver). This way we can choose prediction mode per request. If no prediction mode selected, full prediction mode will be enabled by default (default behavior).

  The tasks property represents various tasks that should be applied to the request. It is a JSON formatted object.

* Create the bsi-cli.conf file as described in configuration section.

* Run the CLI to submit the audio files:

  ```
  behavioral_signals_cli --config [configuration_file] send_audio [csv_file] [pids_log]
  ```

  The [pids_log] file is created automatically and stores the unique ids of the successfully created jobs, which are necessary in order to get the results.


##### Prediction Mode - Support per request mode (Optional)
For every request that we do to the API we can choose whether we want to use Oliver only, ASR only, Diarization only or Oliver+ASR. We can indicate it in our .csv file using the values "audio" for Oliver only, "transcription" for ASR only, "diarization" for Diarization only or "full" for using Oliver+ASR. If we omit the column in our .csv, prediction mode defaults to full.


##### Tasks - Apply tasks on request
We can apply various tasks on each request by adding a

```
{"tasks":[]}
```

entry containing a list of tasks you wish to activate. The currently supported tasks are:

* PII Redaction: `{"name": "piiRedaction", "options": {"replacement": "[pii]"}}`
* Signal Diarization (ignored for stereo files): `{"name": "diarization", "options": {"activate": false}}`

An example of activating the PII redaction task appears below:

```
{"tasks":[{"name": "piiRedaction", "options": {"replacement": "[pii]"}}]}
```

Keep in mind that the JSON above must be wrapped with single quotes in the .csv file.


#### Get results from the Behavioral Signals API

* Run the CLI to get the emotion/behavior recognition call-level overview, diarization and other results:
  ```
  behavioral_signals_cli --config [configuration_file] get_results [pids_log] [results_dir]
  ```

  The results will be written as .json files inside [results_dir] (polling may be performed if results
  are not readily available).

* Run the CLI to get frame-level results:
  ```
  behavioral_signals_cli --config [configuration_file] get_results_frames [pids_log] [results_dir]
  ```

  The results will be written as "[filename]_[pid]_frames.json" files inside [results_dir] (polling may be performed if results are not readily available). You can optionally pass --csv parameter to receive the results in csv format.

* Run the CLI to extract features:
  ```
  behavioral_signals_cli --config [configuration_file] get_results_features [pids_log] [results_dir]
  ```

  The results will be written as "[filename]_[pid]_features.json" files inside [results_dir] (polling may be performed if results are not readily available). You can optionally pass --csv parameter to receive the results in csv format.

* Run the CLI to get ASR results:
  ```
  behavioral_signals_cli --config [configuration_file] get_results_asr [pids_log] [results_dir]
  ```

  The results will be written as "[filename]_[pid]_words.json" files inside [results_dir] (polling may be performed if results are not readily available).

* Run the CLI to get Diarization results:
  ```
  behavioral_signals_cli --config [configuration_file] get_results_diarization [pids_log] [results_dir]
  ```

  The results will be written as "[filename]_[pid]_diarization.json" files inside [results_dir] (polling may be performed if results are not readily available).


#### You may use bsi-cli as an alias to behaviorals_signals_cli

#### Getting Help
```
behavioral_signals_cli --help  or  bsi-cli --help
```



Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
