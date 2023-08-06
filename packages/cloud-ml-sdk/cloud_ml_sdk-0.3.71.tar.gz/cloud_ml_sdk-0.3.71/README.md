# Xiaomi Cloud-ml SDK

## Introduction

It is the Python SDK and command-line tool for Xiaomi cloud-ml service.

## Installation

Install with `pip`.

```
pip install cloud-ml-sdk
```

Install from source.

```
python ./setup install
```

## Configure

Run `cloudml config init` to do the init configuration, including:

- access key and secret key
- FDS if needed
- HDFS if needed
- CloudML cluster endpoint

__NOTE:__ we do support `multi-context` in config management. [More details](#cloudml-multi-context-support)

If you like, you could directly modify the configuration file at `~/.config/xiaomi/config`.

Below is a sample config with two contexts named `c4` and `wuqing` stands for different `cloudml` clusters:

```
{
    // FDS config, can be set via `cloudml config init fds`
    "xiaomi_access_key_id": "AKExxxxxxxxxxxxJJY",
    "xiaomi_secret_access_key": "HLLxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxes1",
    "xiaomi_fds_endpoint": "cnbj1-fds.api.xiaomi.net",
    // CloudML config, mulit context can be set via re-run `cloudml config init`
    "xiaomi_cloudml": {
        "c4": {
            "cloudml_default_fds_bucket": "cloudml-test",
            "xiaomi_secret_access_key": "HLLxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxes1",
            "xiaomi_access_key_id": "AKExxxxxxxxxxxxJJY",
            "xiaomi_cloudml_endpoint": "cnbj3-cloud-ml.api.xiaomi.net",
            "xiaomi_org_mail": "xxx@xiaomi.com"
        },
        "wuqing": {
            "xiaomi_org_mail": "xxx@xiaomi.com",
            "cloudml_default_fds_bucket": "cloudml-test",
            "xiaomi_access_key_id": "AKExxxxxxxxxxxxJJY",
            "xiaomi_cloudml_endpoint": "cnbj2-cloud-ml.api.xiaomi.net",
            "xiaomi_secret_access_key": "HLLxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxes1"
        },
        "default_config_context": "wuqing"
    },
    // HDFS config, can be set via `cloudml config init hdfs`
    "xiaomi_hdfs_krb_account": "your_account_name",
    "xiaomi_hdfs_krb_password": "xxx",
    "xiaomi_hdfs_endpoint": "your_hdfs_ep"
}
```

Or export the access key and secret as environment variables.

```
export XIAOMI_CLOUDML_ENDPOINT="https://cnbj3-cloud-ml.api.xiaomi.net"
export XIAOMI_ACCESS_KEY_ID="AKPFUxxxxxxIPKVG"
export XIAOMI_SECRET_ACCESS_KEY="JDv8ExxxxxxxxxxxxxxrLsuB"
```

## Python SDK

You can use the SDK to access Xiaomi cloud-ml service.

```
from cloud_ml_sdk.client import CloudMlClient
from cloud_ml_sdk.models.train_job import TrainJob

client = CloudMlClient()

train_job = TrainJob(
    "linear",
    "trainer.task",
    "fds://cloud-ml/trainer-1.0.tar.gz")

client.submit_train_job(train_job)
```

## Command-line

You can use the command-line tool to access Xiaomi cloud-ml service.

```
cloudml jobs submit -n $name -m $module -u $url

cloudml jobs list

cloudml jobs describe $name

cloudml jobs events $name

cloudml jobs logs $name

cloudml jobs delete $name
```

## CloudML multi context support

The `context` could be different `cloudml` clusters like `C4` or `Wuqing`, or
different `AK/SK` for different teams so you could have different resource quotas or
access to different `FDS buckets`.

CloudML support multi-context management, including multi-context config and run commands on specified config context.

NOTE(xychu): To keep FDS client(which uses the same config file as `cloudml` does) works,
we still set `AK/SK` and `FDS endpoint` config items in the root level of the default config file
`~/.config/xiaomi/config`, same as HDFS related configs. Which means the current multi-context
is mainly about CloudML itself, like C4&Wuqing clusters or multi-team support.

Currently, the most common use case is multi CloudML cluster config, you could manage tasks in both `c4` and `wuqing` cluster.

### CloudML multi-cluster config

When run `cloudml config init`, there will be two major differences then before:

- you need to name your CloudML config context, and
- you will chose your `default_config_context`

As a result your CloudML config will be like:

```
    // CloudML config, mulit context can be set via re-run `cloudml config init`
    "xiaomi_cloudml": {
        "c4": {
            "cloudml_default_fds_bucket": "cloudml-test",
            "xiaomi_secret_access_key": "HLLxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxes1",
            "xiaomi_access_key_id": "AKExxxxxxxxxxxxJJY",
            "xiaomi_cloudml_endpoint": "cnbj3-cloud-ml.api.xiaomi.net",
            "xiaomi_org_mail": "xxx@xiaomi.com"
        },
        "wuqing": {
            "xiaomi_org_mail": "xxx@xiaomi.com",
            "cloudml_default_fds_bucket": "cloudml-test",
            "xiaomi_access_key_id": "AKExxxxxxxxxxxxJJY",
            "xiaomi_cloudml_endpoint": "cnbj2-cloud-ml.api.xiaomi.net",
            "xiaomi_secret_access_key": "HLLxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxes1"
        },
        "default_config_context": "wuqing"
    }
```

The config above means that you have two cloudml config contexts named as "c4" and "wuqing" respectively.
And your default config context is "wuqing".

You can change your default config context to "c4" by:

```bash
cloudml config set_default c4
```

Besides, you could view your current config anytime via:

```bash
cloudml config show
```

### CloudML multi-cluster commands

With multi-cluster configured, you'll get the power to manage your tasks in all of them.

For resources in your default cluster, no changes is needed, just as before:

```bash
# list all the train jobs using the default CloudML config context, which is named "wuqing"
cloudml jobs list
# same CloudML config for all other commands when no context argument(`-k/--context`) given
cloudml dev list

cloudml quota list
```

When you want to control things in other clusters, we support one global argument `-k/--context` to specify
which CloudML config context you'd like to use.

```bash
# list all the train jobs using the CloudML config context named "c4"
cloudml -k c4 jobs list
# works for other commands as well
cloudml --context c4 dev list

cloudml -k c4 quota list
```

NOTE(xychu): if you want to use context other than default one, the global argument(`-k/--context`)
**need to** put before all the sub-commands. Otherwise, it will **not** be recognized correctly.
