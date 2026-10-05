import os

import icechunk
import netCDF4
import rasterio

# S3 endpoint of our object store
ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL")

# S3 bucket used in the workshop
BUCKET = "cng-forum-workshop"
BUCKET_URI = f"s3://{BUCKET}"

# Set prefix where the current user can write to
USER_NAME = os.getenv("JUPYTERHUB_USER") or os.getenv("USER")
USER_PREFIX_URI = f"{BUCKET_URI}/users/{USER_NAME}"


def https_url(urlpath: str) -> str:
    """Convert s3://bucket/key to the public (path-style) HTTPS URL."""
    return f"{ENDPOINT_URL}/{urlpath.removeprefix('s3://')}"


def gdal_env(**kwargs) -> rasterio.Env:
    """GDAL environment to read from/write to the object store."""
    return rasterio.Env(
        AWS_S3_ENDPOINT=ENDPOINT_URL,
        AWS_VIRTUAL_HOSTING=False,
        **kwargs,
    )


def vsis3(urlpath: str) -> str:
    """Convert s3://bucket/key to the GDAL virtual file system path /vsis3/bucket/key."""
    return f"/vsis3/{urlpath.removeprefix('s3://')}"


def print_raster_info(urlpath: str) -> None:
    """Print raster information for a file."""
    urlpath = urlpath if urlpath.startswith("s3://") else f"s3://{urlpath}"
    with gdal_env(), rasterio.open(urlpath) as src:
        print("URL:         ", src.name)
        print("Driver:      ", src.driver)
        print("Size:        ", src.width, "x", src.height, ", Bands:", src.count)
        print("CRS:         ", src.crs)
        print("Bounds:      ", src.bounds)
        print("Resolution:  ", src.res)
        print("Dtypes:      ", src.dtypes)
        print("Nodata:      ", src.nodata)
        print("Block shapes:", src.block_shapes)
        print("Tiled:       ", src.profile.get("tiled", False))
        print("Compression: ", src.compression.name.upper() if src.compression else None)
        print("Layout:      ", src.tags(ns="IMAGE_STRUCTURE").get("LAYOUT"))
        print("Bands:       ")
        for i in range(src.count):
            print(f" * Band {i + 1}: description={src.descriptions[i]}, overviews={src.overviews(i + 1)}")


def print_netcdf_info(urlpath: str) -> None:
    """Print structure information for a NetCDF file."""
    urlpath = urlpath if urlpath.startswith("https://") else https_url(urlpath)
    with netCDF4.Dataset(f"{urlpath}#mode=bytes", mode="r") as ds:  # force byte-range HTTP reads
        print("URL:         ", urlpath)
        print("Format:      ", ds.data_model)
        print("Dimensions:  ", {name: len(dim) for name, dim in ds.dimensions.items()})
        print("Variables:   ")
        for name, var in ds.variables.items():
            print(
                f" * {name}: dtype={var.dtype}, dims={var.dimensions}, shape={var.shape}, "
                f"chunking={var.chunking()}, filters={var.filters()}"
            )


def icechunk_repo(urlpath: str) -> icechunk.Repository:
    """Open (or create) an Icechunk repository, allowing virtual chunks from the source bucket."""
    bucket, _, prefix = urlpath.removeprefix("s3://").partition("/")
    region = os.getenv("AWS_REGION")
    storage = icechunk.s3_storage(
        bucket=bucket,
        prefix=prefix,
        endpoint_url=ENDPOINT_URL,
        region=region,
        force_path_style=True,
        from_env=True,
    )
    config = icechunk.RepositoryConfig.default()
    config.set_virtual_chunk_container(
        icechunk.VirtualChunkContainer(
            f"s3://{bucket}/",
            icechunk.s3_store(
                region=region, 
                endpoint_url=ENDPOINT_URL, 
                force_path_style=True
            ),
        )
    )
    credentials = icechunk.containers_credentials(
        {f"s3://{bucket}/": icechunk.s3_credentials(anonymous=True)}
    )
    return icechunk.Repository.open_or_create(
        storage, config, authorize_virtual_chunk_access=credentials
    )
