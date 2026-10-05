# Building and Benchmarking Cloud-Optimized Geospatial Raster and Tensor Datasets

Material for the [CNG Forum 2026] workshop @ Snowbird, Utah.

[CNG Forum 2026]: https://2026.cloudnativegeo.org/

## Overview

A hands-on workshop on (i) generating cloud-optimized versions of existing raster and multi-dimensional datasets, and (ii) benchmarking them in a transparent and reproducible way. We start from public datasets from [PDOK](https://www.pdok.nl) (AHN-4 elevation model, aerial images) and [KNMI](https://dataplatform.knmi.nl) (gridded daily temperature):

| Notebook | Content |
|---|---|
| [`00-setup`](notebooks/00-setup.ipynb) | Environment and object-store access |
| [`01-explore-datasets`](notebooks/01-explore-datasets.ipynb) | The original datasets: what makes them (not) cloud-native? |
| [`02-convert-rasters`](notebooks/02-convert-rasters.ipynb) | GeoTIFF → Cloud-Optimized GeoTIFF: block size, compression, overviews |
| [`03-convert-knmi`](notebooks/03-convert-knmi.ipynb) | NetCDF → Zarr: chunk layouts, sharding, virtual Zarr with VirtualiZarr and Icechunk |
| [`04-benchmark`](notebooks/04-benchmark.ipynb) | Benchmark access patterns with [cloudgeometer](https://github.com/CLOUD-NES/cloudgeometer): time, requests, bytes |
| [`05-stac`](notebooks/05-stac.ipynb) | Publish a static STAC catalog and stac-geoparquet |

The workshop builds on the experience of the CLOUD-NES project.

