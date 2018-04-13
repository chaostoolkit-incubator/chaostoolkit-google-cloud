# Chaos Toolkit Extension for Google Cloud Engine

[![Build Status](https://travis-ci.org/chaostoolkit-incubator/chaostoolkit-google-cloud.svg?branch=master)](https://travis-ci.org/chaostoolkit-incubator/chaostoolkit-google-cloud)
[![Python versions](https://img.shields.io/pypi/pyversions/chaostoolkit-google-cloud.svg)](https://www.python.org/)

This project is a collection of [actions][] and [probes][], gathered as an
extension to the [Chaos Toolkit][chaostoolkit]. It targets the
[Google Cloud Engine][gce] platform.

[actions]: http://chaostoolkit.org/reference/api/experiment/#action
[probes]: http://chaostoolkit.org/reference/api/experiment/#probe
[chaostoolkit]: http://chaostoolkit.org
[gce]: https://cloud.google.com/compute/

## Install

This package requires Python 3.5+

To be used from your experiment, this package must be installed in the Python
environment where [chaostoolkit][] already lives.

```
$ pip install -U chaostoolkit-google-cloud
```

## Usage

To use the probes and actions from this package, add the following to your
experiment file:

```json
{
    "type": "action",
    "name": "swap-nodepool-for-a-new-one",
    "provider": {
        "type": "python",
        "module": "chaosgce.nodepool.actions",
        "func": "swap_nodepool",
        "secrets": ["gce"],
        "arguments": {
            "body": {
                "nodePool": {
                    "config": { 
                        "oauthScopes": [
                            "gke-version-default",
                            "https://www.googleapis.com/auth/devstorage.read_only",
                            "https://www.googleapis.com/auth/logging.write",
                            "https://www.googleapis.com/auth/monitoring",
                            "https://www.googleapis.com/auth/service.management.readonly",
                            "https://www.googleapis.com/auth/servicecontrol",
                            "https://www.googleapis.com/auth/trace.append"
                        ]
                    },
                    "initialNodeCount": 3,
                    "name": "new-default-pool"
                }
            }
        }
    }
}
```

That's it!

Please explore the code to see existing probes and actions.


## Configuration

### Project and Cluster Information

You can pass the context via the `configuration` section of your experiment:

```json
{
    "configuration": {
        "gce_project_id": "...",
        "gce_cluster_name": "...",
        "gce_region": "...",
        "gce_zone": "..."
    }
}
```

Note that most functions exposed in this package also take those values
directly when you want specific values for them.

### Credentials

This extension expects a [service account][sa] with enough permissions to
perform its operations. Please create such a service account manually (do not
use the default one for your cluster if you can, so you'll be able to delete
that service account if need be).

[sa]: https://developers.google.com/api-client-library/python/auth/service-accounts#creatinganaccount

Once you have created your service account, either keep the file on the same
machine where you will be running the experiment from. Or, pass its content
as part of the `secrets` section, although this is not recommended because your
sensitive data will be quite visible.

Here is the first way:

```json
{
    "secrets": {
        "gce": {
            "service_account_file": "/path/to/sa.json"
        }
    }
}
```

While the embedded way looks like this:


```json
{
    "secrets": {
        "gce": {
            "service_account_info": {
                "type": "service_account",
                "project_id": "...",
                "private_key_id": "...",
                "private_key": "...",
                "client_email": "...",
                "client_id": "...",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://accounts.google.com/o/oauth2/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/...."
            }
        }
    }
}
```


### Putting it all together

Here is a full example:

```json
{
    "version": "1.0.0",
    "title": "...",
    "description": "...",
    "configuration": {
        "gce_project_id": "...",
        "gce_cluster_name": "...",
        "gce_region": "...",
        "gce_zone": "..."
    },
    "secrets": {
        "gce": {
            "service_account_file": "/path/to/sa.json"
        }
    },
    "method": [
        {
            "type": "action",
            "name": "swap-nodepool-for-a-new-one",
            "provider": {
                "type": "python",
                "module": "chaosgce.nodepool.actions",
                "func": "swap_nodepool",
                "secrets": ["gce"],
                "arguments": {
                    "body": {
                        "nodePool": {
                            "config": { 
                                "oauthScopes": [
                                    "gke-version-default",
                                    "https://www.googleapis.com/auth/devstorage.read_only",
                                    "https://www.googleapis.com/auth/logging.write",
                                    "https://www.googleapis.com/auth/monitoring",
                                    "https://www.googleapis.com/auth/service.management.readonly",
                                    "https://www.googleapis.com/auth/servicecontrol",
                                    "https://www.googleapis.com/auth/trace.append"
                                ]
                            },
                            "initialNodeCount": 3,
                            "name": "new-default-pool"
                        }
                    }
                }
            }
        }
    ]
}
```

## Contribute

If you wish to contribute more functions to this package, you are more than
welcome to do so. Please, fork this project, make your changes following the
usual [PEP 8][pep8] code style, sprinkling with tests and submit a PR for
review.

[pep8]: https://pycodestyle.readthedocs.io/en/latest/

The Chaos Toolkit projects require all contributors must sign a
[Developer Certificate of Origin][dco] on each commit they would like to merge
into the master branch of the repository. Please, make sure you can abide by
the rules of the DCO before submitting a PR.

[dco]: https://github.com/probot/dco#how-it-works

### Develop

If you wish to develop on this project, make sure to install the development
dependencies. But first, [create a virtual environment][venv] and then install
those dependencies.

[venv]: http://chaostoolkit.org/reference/usage/install/#create-a-virtual-environment

```console
$ pip install -r requirements-dev.txt -r requirements.txt 
```

Then, point your environment to this directory:

```console
$ python setup.py develop
```

Now, you can edit the files and they will be automatically be seen by your
environment, even when running from the `chaos` command locally.

### Test

To run the tests for the project execute the following:

```
$ pytest
```
