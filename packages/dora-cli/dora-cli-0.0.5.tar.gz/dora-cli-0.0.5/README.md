# Dora CLI

Command Line Interface to manager an Dora sandbox.

```sh
python -m dora_cli
```

## Usage 

The following options are available in this version:

## `configure`

Use to setup your environment with all the credentials and configurations needed to access the Cloud Provider services.

All the configurations will be saved on `~/.config/dora-cli/config.json`

> Use `--help` option to more details

## `start`

If successful you will be prompted with the **token** generated to access you Jupyter Lab environment followed by **name** and **status** of the *container*.

```txt
TOKEN:d337b5ee0b72c6687b9a9e8f8f9a2f5972559454e90c6e10
happy_lovelace:created
```

Access the application by `http://<public-ip>:8888/lab?token=d337b5ee0b72c6687b9a9e8f8f9a2f5972559454e90c6e10`

> Use `--help` option to more details


## Requirements

The following packages are needed on the Operating System to run this application:

- python3.7
- pip 
- docker 
- nfs-common

```sh
# setup on Ubuntu linux
sudo apt install -y python3 python3-pip python3-setuptools docker.io nfs-common
```

> [Mounting an NFS File System to ECSs (Linux)](https://support.huaweicloud.com/intl/en-us/qs-sfs/en-us_topic_0034428728.html)
