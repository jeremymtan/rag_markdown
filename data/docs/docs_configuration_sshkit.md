---
# This file has been generated from the Kamal source, do not edit directly.
# Find the source of this file at lib/kamal/configuration/docs/sshkit.yml in the Kamal repository.
title: SSHKit
---

# SSHKit

[SSHKit](https://github.com/capistrano/sshkit) is the SSH toolkit used by Kamal.

The default, settings should be sufficient for most use cases, but
when connecting to a large number of hosts, you may need to adjust.

## [SSHKit options](#sshkit-options)

The options are specified under the sshkit key in the configuration file.

```yaml
sshkit:
```

## [Max concurrent starts](#max-concurrent-starts)

Creating SSH connections concurrently can be an issue when deploying to many servers.
By default, Kamal will limit concurrent connection starts to 30 at a time.

```yaml
  max_concurrent_starts: 10
```

## [Pool idle timeout](#pool-idle-timeout)

Kamal sets a long idle timeout of 900 seconds on connections to try to avoid
re-connection storms after an idle period, such as building an image or waiting for CI.

```yaml
  pool_idle_timeout: 300
```
