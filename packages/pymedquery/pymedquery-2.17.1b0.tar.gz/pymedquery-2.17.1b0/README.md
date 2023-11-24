# pyMedQuery [<img align="right" width="120" alt="20200907_104224" src="https://user-images.githubusercontent.com/29639563/183247351-53e45de2-09cf-4344-be30-120d8a744d5f.png">](https://neomedsys.io/)

[![py-medquery](https://github.com/CRAI-OUS/py-medquery/actions/workflows/pymedquery.yaml/badge.svg)](https://github.com/CRAI-OUS/py-medquery/actions/workflows/pymedquery.yaml) <img src="./pymedquery/docs/coverage.svg"> [![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![PyPI status](https://img.shields.io/pypi/status/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)

<br>

*pyMedQuery* is the sweet sweet database client for python that allows authenticated users to access medical data in the database MedQuery. The main reason for *pyMedQuery* to exist is to efficiently enable database access via python code that can be integrated into machine learning projects, production systems and data analysis pipelines. We are using SSL/TLS for safe connections and client certifications for authentication in order to keep the database connection highly secure. 

The average user is expected to instantiate the `PyMedQuery()` class and run the methods `extract` or `batch_extract` to extract the necessary data for their given project. If the user wants to use the default SQL script then set the argument `get_all` to true in the `(batch_)extract` method and specify which projectID the data should relate to. The method will then extract all the data belonging to that projectID. Other users might find it usefull to write custom SQL scripts where the argument `format_params` can be passed into the extraction for flexible formating of SQL queries. This is especially useful for applications and pipelines.

If you have any feedback or ideas to new features or bugs then please get in contact with us.

*pyMedQuery* is meant to be a simple and friendly. We hope you'll like it! Check out the tutorial script for some examples. 

### Quickstart Guide

#### 1. installing and completing the settings (this is a one time procedure)

1. Use poetry or any other kind of dependency manager to install the package.

```$ poetry add pymedquery```

2. If you are using poetry then run `poetry run pymq-init` and follow the setup of the database authentication. (A valid username, password and cert files are currently required in forehand) The setup script will guide you through the authentication. A more streamlined way to authenticate via a MedQuery's CLI is in the roadmap for 2022.

<details>
<summary>Open this drop down if you want to do the authentication manually or you are on Windows with no bash in power shell:</summary>
<br>

2. Store the certification and key files for postgres somwhere safe on your machine. (you will receive the database credentials from the admins)

3. Set environment variables on your system for the file paths that point to the cert and key files you received for the database. We recommended to put the commands in your .zshrc or .bashrc.

```
$ echo 'export PGSSLCERT=file_path_to_client_crt' >> ~/<.your_rc_file>
$ echo 'export PGSSLROOTCERT=file_path_to_ca_crt' >> ~/<.your_rc_file>
$ echo 'export PGSSLKEY=file_path_to_client_key' >> ~/<.your_rc_file>
```

Set correct permissions on your client key in order for the database to read it.
```
$ chmod 600 $PGSSLKEY
```

Do the equivalent on windows with

```
setx PGSSLCERT file_path_to_client_crt
setx PPGSSLROOTCERT file_path_to_ca_crt
setx PGSSLKEY file_path_to_client_key
```

<details>
<summary>Windows is not a straight forward when setting 600 permission but you can follow these steps:</summary>
<br>

- Right-click on the target file and select properties then select Security Tab

- Click Advanced and then make sure inheritance is disabled.

- Click apply and then click Edit in the security menu

- Remove all users except Admin user, which should have full control *Admin account should have all checkboxes checked on Allow column except special permission.

- Click Apply and then click OK :)
        
<br>
</details>


4. Also include the username and password in your rc file as environment variables:

```
<your-rc-file>
# (env vars to fill out that pyMedQuery will pick up on)
export MQUSER='username-to-medquery'
export MQPWD='password-to-medquery'
export DATABASE='medquery'
```
##### NOTE! The env var names is a strict convention. The program will not work if you use other names.

<br>
</details>

#### 2. Examples of how to run the basics

0.  Extracting a small data sample by using the default SQL script and a certain `project_id`. Given that `get_all` is true then you can adjust
        how many patients to include in your query by filling in limit. If you leave it blank then the query will retrieve all records in the
        `project_id`. If the data has corresponding masks, then set `include_mask` to true

```python
from pymedquery import pymq
        
# instantiate the class
mq = pymq.PyMedQuery()
# Use the limit argument to set a maximum number of patients to include in the extraction
small_data_sample = mq.extract(get_all=True, get_affines=True, project_id='fancyID', limit=200, include_mask=False)
        # do more stuff here
        # save processed data to your local disk with e.g. in HDF5 or pickle. Let go of big cluttering file systems!
```


1.  Extracting a small data sample with a custom and formatable SQL script where data has corresponding masks.
        A mask in this case is a finished image segmentation.

```python
from pymedquery import pymq
from config import config

sql_file_path =  # file-path-to-the-pre-written-sql-script
# instantiate the class
mq = pymq.PyMedQuery()
        
# The formatable parameters will be inserted into the custom SQL scrip and thus extracting data belonging to
# 'fancy_id' from only the year 2012 and for only women between 40 and 49. The SQL script must include the
# format syntax {project_id}, {start_time}..., etc. for the filtering to happen.
FORMAT_PARAMS = {
        'project_id': 'fancy_id',
        'start_time': '2012-01-01',
        'end_time': '2012-12-31',
        'gender': 'F',
        'age_group': '40-49'
        }
        
# Note that the SQL file path is given by a configuartion script called config
# Lets set get_affines to False in order to include the affine matrices as well
small_data_sample = mq.extract(get_all=False, get_affines=False, format_params=FORMAT_PARAMS, sql_file_path=config.SQL_FILE_PATH, include_mask=True)
        # do more stuff
        # save processed data to local disk with e.g. in HDF5 orpickle
```
        
2. Extracting large amounts of data (this step could either be done with a custom SQL file or without. The example is given with the default SQL file for brevity.

```python
from pymedquery import pymq

# instantiate the class
mq = pymq.PyMedQuery()

# Setting batch size to 200 volumes with 150 slices each. That corresponds to 30000 2D images in each batch
large_data = mq.batch_extract(get_all=True, project_id='fancyID', batch_size=200)
for batch in large_data:
        # do more stuff here:
        # 1. process data
        # 2. split train, test and val
        # 3. save processed data to your local disk with e.g. HDF5
```
##### NOTE: it's advisable to save your processed data in a HDF5 file as it's easy to structure your data in the file and it can be lazy loaded into other scripts for subsequent analyses.
        
3. Uploading data into MedQuery. You can either create your own table in a specific part of MedQuery or use a pre-existing table (there will be tables for the data and model versioning and storing)

```python
from pymedquery import pymq

# instantiate the class
mq = mq.PyMedQuery()
 
# load the model file into the program
model_file = load_model()

# We are done with a model and I we want to save it back to MedQuery with the proper version for other researchers and applications to use.
# Befor we make the upload, we need to have dictionary containing the records to upload. The dictionary keys must align with sorting of the table coulumns. Make sure that this is correct befor uploading. Use the 'verbose' argument if you want to make sure that you structure is correct.
# the structure of the records dict should be: {key: (record_value, blob),....}
records Dict[str, Tuple[Any, Any]: = {
        # record_value: blob (not all record_values have a corresponding blob)
        'timestamp': (datetime.datetime.now(), None),
        'model_id': ('model_fasde32r345t45c324xd', model_file),
        'model_version': ('modelw_v1.1.0', None),
        'project_owner': ('Schlomo Cohen': None)
        }

 
# Upload the records with pymedquery
mq.upload(records=records, table_name='model_artifacts', verbose=True, image_extraction=False)
          
# NOTE! Blobs for record_values are not supported at the moment
```

##### The records dict aligns with the `model_artifacts` table which has the following columns:
        
      | time | model_id | model_version | project_owner |

##### The project pyMedQuery is currently in Beta and we are looking for Beta tester. You have to be affiliated or employed at UHO to take part in the Beta release
