# gateway-api charts

Helm charts for installing Kubernetes
[Gateway-API](https://gateway-api.sigs.k8s.io/) CRDs.

## Usage

To install the standard channel CRDS:

```shell
helm install gateway-api-crds oci://ghcr.io/ucl-arc-environments/charts/standard-gateway-api-crds
```

To install the experimental channel CRDs:

```shell
helm install gateway-api-crds oci://ghcr.io/ucl-arc-environments/charts/experimental-gateway-api-crds
```

> [!CAUTION]
> Uninstalling the Helm release WILL NOT remove the CRDs from the
> cluster. Similarly, running `helm upgrade` will not upgrade the currently
> deployed CRDs. In order to upgrade you will first need to completely remove
> the currently deployed CRDs before running `helm install`. If you proceed to
> upgrade the CRDs on your cluster, note that there will be potential for
> deployed resources to become unusable.
>
> See [this note in the Helm documentation about
> CRDs](https://helm.sh/docs/chart_best_practices/custom_resource_definitions/)
> before proceeding.

## Version updates

[Renovate](https://docs.renovatebot.com/) is used in this repository to track
the gateway-api version in the `Chart.yaml` files and as well as the
[Makefile](./scripts/Makefile). This will create pull requests to update the
version number in these files. This will trigger the
[update.yaml](.github/workflows/update.yaml) workflow, which will run the
provided Python script to download and update the CRD files in the repository.
Merging and creating a Github release will then push the new charts to the
`ghcr.io` registry.

If manually updating the CRD files using the Python scripts (via the `Makefile`
for convenience), make sure to update the `appVersion` and `GATEWAY_API_VERSION`
variable in the `Makefile`.
