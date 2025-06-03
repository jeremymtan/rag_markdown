---
title: "Kamal 2: Upgrade Guide"
---

# Kamal 2: Upgrade Guide

There are some significant differences between Kamal 1 and Kamal 2.

- The Traefik proxy has been [replaced by kamal-proxy](../proxy-changes).
- Kamal will run all containers in a [custom Docker network](../network-changes).
- There are some backward-incompatible [configuration changes](../configuration-changes).
- How we pass secrets to containers [has changed](../secrets-changes).

If you want to continue using Traefik, you can run it as an accessory; see [here](../continuing-to-use-traefik) for more details.

## [Upgrade steps](#upgrade-steps)

### Upgrade to Kamal 1.9.x

If you are planning to do in-place upgrades of servers, you should first upgrade to Kamal 1.9, as it has support for downgrading.

If using the gem directly, you can run:

```bash
gem install kamal --version 1.9.0
```

Confirm you can deploy your application with Kamal 1.9.

### Upgrade to Kamal 2

If using the gem directly, run:

```bash
gem install kamal
```

### Make configuration changes

You'll need to [convert your configuration](../configuration-changes) to work with Kamal 2.

You can test whether the new configuration is valid by running:

```bash
$ kamal config
```

If you have multiple destinations, you should test each ones configuration:

```bash
$ kamal config -d staging
$ kamal config -d beta
```

### Move from .env to .kamal/secrets

Follow the steps [here](../secrets-changes).

### Verify container port

The default app port was [changed from 3000 to 80](https://kamal-deploy.org/docs/upgrading/configuration-changes/#traefik-to-proxy), you'll need to either specify your `app_port` or update your `EXPOSE` port if not using port 80.

## [In-place upgrades](#in-place-upgrades)

**Warning: Test this in a non-production environment first, if possible.**

### Upgrading

You can then upgrade with:

```
$ kamal upgrade [-d <DESTINATION>]
```

You'll need to do this separately for each destination.

The `kamal upgrade` command will:

1. Stop and remove the Traefik proxy.
2. Create a `kamal` Docker network if one doesn't exist.
3. Start a `kamal-proxy` container in the new network.
4. Reboot the currently deployed version of the app container in the new network.
5. Tell `kamal-proxy` to send traffic to it.
6. Reboot all accessories in the new network.

### Avoiding downtime

If you are running your application on multiple servers and want to avoid downtime, you can do a rolling upgrade:

```bash
$ kamal upgrade --rolling [-d <DESTINATION>]
```

This will follow the same steps as above, but host by host.

Alternatively, you can run the command host by host:

```bash
$ kamal upgrade -h 127.0.0.1[,127.0.0.2]
```

You could additionally use the [pre-proxy-reboot](../hooks/pre-proxy-reboot.md) and [post-proxy-reboot](../hooks/post-proxy-reboot.md) hooks to manually remove your server from upstream load balancers, to ensure no requests are dropped during the upgrade process.

### Downgrading

If you want to reverse your changes and go back to Kamal 1.9:

1. Uninstall Kamal 2.0.
2. Confirm you are running Kamal 1.9 by running `kamal version`.
3. Run the `kamal downgrade` command. It has the same options as `kamal upgrade` and will reverse the process.

The upgrade and downgrade commands can be re-run against servers that have already been upgraded or downgraded.
