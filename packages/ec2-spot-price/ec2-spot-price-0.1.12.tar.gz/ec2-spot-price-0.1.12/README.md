# ec2-spot-price

Library and command for retrieving Amazon EC2 spot instance price


## Install

```sh
pip install ec2-spot-price
```

## Setup

You need to have IAM user to access EC2's DescribeSpotPriceHistory API.
A simple way to do is to add new user and attach AmazonEC2ReadOnlyAccess
policy.

Or you can use existent user which have permissions to access that API.

### Goto IAM Console

https://console.aws.amazon.com/iam/home

### Add new IAM user

```
User name: myuser  # whatever you want
Access type: Programmatic access
Set permissions: Attach existing policies directly
Policy name: AmazonEC2ReadOnlyAccess
Download .csv
```

### Edit ~/.aws/credentials

You can use "named profile" to have multiple credentials settings.
See https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html

```
[myprofile]  # or [default]
aws_access_key_id=[copy from csv]
aws_secret_access_key=[copy from csv]
region=us-east-2  # wherever you want
```

## Usage

Run Script

If you use [myprofile], you need to specify AWS_PROFILE environment
variable.

```
export AWS_PROFILE=myprofile
python ec2_spot_price.py -i g3.4xlarge,p2.xlarge
```

If you use [default] section, you can omit AWS_PROFILE.

```
python ec2_spot_price.py -i g3.4xlarge,p2.xlarge
```

## See also

https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeSpotPriceHistory.html
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration
https://aws.amazon.com/ec2/spot/pricing/


## Author

Susumu OTA


