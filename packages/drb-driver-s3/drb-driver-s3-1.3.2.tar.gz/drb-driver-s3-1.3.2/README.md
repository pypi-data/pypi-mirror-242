# Amazon simple storage service driver

This drb-driver-s3 module implements S3 protocol access with DRB data model.

## S3 Factory and S3 Node
The module implements the factory model defined in DRB in its node resolver. Based on the python entry point mechanism, this module can be dynamically imported into applications.

The entry point group reference is `drb.drivers.aws3`.<br/>
The driver name is `aws3`.<br/>
The factory class is encoded into `drb.driver.aws3`.<br/>
The S3 signature id is  `4ab73f92-bbff-11ec-8422-0242ac120002`.<br/>


## Using this module
The project is present in https://www.pypi.org service. it can be freely 
loaded into projects with the following command line:

```commandline
pip install drb-driver-aws3
```
## Access Data
`DrbS3Node` manages the s3 protocol to access remote data. The construction
parameter is an authentication object.

```python
from drb.drivers.aws3 import DrbS3Service, Auth
from botocore.config import Config

auth = Auth(service_name='s3',
            endpoint_url='http://your_s3_storage/',
            aws_access_key_id='user',
            aws_secret_access_key='password',
            config=Config(signature_version='s3v4'),
            region_name='us-east-1')
node = DrbS3Service(auth)
```
When accessing a DrbS3Service the node gives access to all the bucket of this service by giving a list of DrbS3Bucket,
and then each node gives a list of DrbS3Object for each object in the bucket.

## Limitations

This driver doesn't allow to write, modify, delete file on a s3 bucket,
or it doesn't allow to delete or upload a file.
This driver doesn't allow to download directly a bucket.

## Documentation

The documentation of this implementation can be found here https://drb-python.gitlab.io/impl/aws3