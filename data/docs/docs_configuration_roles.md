---
# This file has been generated from the Kamal source, do not edit directly.
# Find the source of this file at lib/kamal/configuration/docs/role.yml in the Kamal repository.
title: Roles
---

# Roles

Roles are used to configure different types of servers in the deployment.
The most common use for this is to run web servers and job servers.

Kamal expects there to be a `web` role, unless you set a different `primary_role`
in the root configuration.

## [Role configuration](#role-configuration)

Roles are specified under the servers key:

```yaml
servers:
```

## [Simple role configuration](#simple-role-configuration)

This can be a list of hosts if you don't need custom configuration for the role.

You can set tags on the hosts for custom env variables (see [Environment variables](../environment-variables)):

```yaml
  web:
    - 172.1.0.1
    - 172.1.0.2: experiment1
    - 172.1.0.2: [ experiment1, experiment2 ]
```

## [Custom role configuration](#custom-role-configuration)

When there are other options to set, the list of hosts goes under the `hosts` key.

By default, only the primary role uses a proxy.

For other roles, you can set it to `proxy: true` to enable it and inherit the root proxy
configuration or provide a map of options to override the root configuration.

For the primary role, you can set `proxy: false` to disable the proxy.

You can also set a custom `cmd` to run in the container and overwrite other settings
from the root configuration.

```yaml
  workers:
    hosts:
      - 172.1.0.3
      - 172.1.0.4: experiment1
    cmd: "bin/jobs"
    options:
      memory: 2g
      cpus: 4
    logging:
      ...
    proxy:
      ...
    labels:
      my-label: workers
    env:
      ...
    asset_path: /public
```
