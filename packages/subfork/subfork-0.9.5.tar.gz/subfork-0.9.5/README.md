Subfork Python API
==================

This package provides the Subfork Python API and command line interface.


Installation
------------

The easiest way to install:

```shell
$ pip install subfork
```

Quick Start
-----------

In order to authenticate with the Subfork API, you will first need to create
API access keys for your site at [subfork.com](https://subfork.com).

To use the Subfork Python API your site must have a verified domain. Then
instantiate a client using the site domain, port, access and secret keys:

```python
import subfork
sf = subfork.get_client(domain, port, access_key, secret_key)
```

Configuration
-------------

Using the Subfork Python API requires basic authentication. To use
environment variables, set the following:

```shell
$ export SUBFORK_HOST=<domain name>
$ export SUBFORK_ACCESS_KEY=<access key>
$ export SUBFORK_SECRET_KEY=<secret key>
```

To use a shared config file, copy the `example_subfork.yaml` file to `subfork.yaml`
at the root of your project and make required updates:

```shell
$ cp example_subfork.yaml subfork.yaml
$ nano subfork.yaml
```

Or set `$SUBFORK_CONFIG_FILE` to the path to `subfork.yaml`:

```shell
$ export SUBFORK_CONFIG_FILE=/path/to/subfork.yaml
```

A minimal `subfork.yaml` config file contains the following values:

```yaml
SUBFORK_HOST: <domain name>
SUBFORK_ACCESS_KEY: <access key>
SUBFORK_SECRET_KEY: <secret key>
```

Site Templates
--------------

Site data is stored in a separate `template.yaml` file and required for
testing and deploying sites.

Required:

- `domain` : the domain or hostname of the site (no http)
- `pages` : named list of site template files and routes

Optional:

- `template_folder` : template folder path (default "templates")
- `static_folder` : static file folder path (default "static")
- `minimize` : minimize file contents if possible

For example:

```yaml
domain: example.fork.io
# template_folder: templates
# static_folder: static
# minimize: true
pages:
  index:
    route: /
    file: index.html
  user:
    route: /user/<username>
    file: user.html
```

Basic Commands
--------------

To deploy a site:

```shell
$ subfork deploy [template.yaml] -c <comment> [--release]
```

To test the site using the dev server:

```shell
$ subfork run [template.yaml]
```

To process tasks:

```shell
$ subfork worker [options]
```

Data
----

Data is organized into `datatypes` and must be JSON serializable. 

Insert a new datatype record, where `datatype` is the name of the
datatype, and `data` is a dictionary:

```python
sf = subfork.get_client()
sf.get_data(datatype).insert(data)
```

Find data matching a list of search `params` for a given `datatype`:

```python
results = sf.get_data(datatype).find(params)
```

where `params` is a list of `[key, op, value]`, for example:

```python
results = sf.get_data(datatype).find([[key, "=", value]])
```

More info can be found using pydoc:

```shell
$ pydoc subfork.api.data
```

Workers
-------

Workers process tasks created either via API clients or users.
By default, running the `subfork worker` command will pull tasks from a
specified queue and process them.

```shell
$ subfork worker [--queue <queue> --func <pkg.mod.func>]
```

For example:

```shell
$ subfork worker --queue test --func subfork.worker.test
```

Workers can also be defined in the `subfork.yaml` file, and can contain
more than one worker specification:

```yaml
WORKER:
  worker1:
    queue: test
    function: subfork.worker.test
  worker2:
    queue: stress
    function: subfork.worker.stress
```

To create a task, pass function kwargs to a named task queue,
for example, passing `t=3` to worker2 defined above:

```python
sf = subfork.get_client()
task = sf.get_queue("stress").create_task({"t": 3})
```

To get the results of completed tasks:

```python
task = sf.get_queue("stress").get_task(taskid)
task.get_results()
```

More info can be found using pydoc:

```shell
$ pydoc subfork.api.task
```

Running a worker as a service:

See the `bin/worker` and `services/worker.service` files for an example of how
to set up a systemd worker service. 

Update the ExecStart and Environment settings with the correct values, and copy
the service file to /etc/systemd/system/ and start the service.

```shell
$ sudo cp services/worker.service /etc/systemd/system/
$ sudo systemctl daemon-reload
$ sudo systemctl start worker
$ sudo systemctl enable worker
```

Checking worker logs:

```shell
$ sudo journalctl -u worker -f
```