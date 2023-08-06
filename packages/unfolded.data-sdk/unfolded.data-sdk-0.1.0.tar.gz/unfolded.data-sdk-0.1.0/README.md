# `unfolded-data-sdk`

Python package for interfacing with Unfolded's Data SDK.

## Installation

For now, this package is not on a public Python package repository. However you
can install it directly from Github easily as long as you have access to the
repository:

```
pip install git+ssh://git@github.com/UnfoldedInc/unfolded-py.git#subdirectory=modules/data-sdk
```

## Usage

### CLI

The CLI is available through `uf-data-sdk` on the command line. Running that
without any other arguments gives you a list of available commands:

```
> uf-data-sdk
Usage: uf-data-sdk [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  delete-dataset    Delete dataset from Unfolded Studio Warning: This...
  download-dataset  Download existing dataset to disk
  list-datasets     List datasets for a given user
  update-dataset    Update data for existing Unfolded Studio dataset
  upload-file       Upload new dataset to Unfolded Studio
```

Then to see how to use a command, pass `--help` to a subcommand:

```
> uf-data-sdk list-datasets --help
Usage: uf-data-sdk list-datasets [OPTIONS]

  List datasets for a given user

Options:
  --token TEXT    Unfolded Studio access token.  [required]
  --baseurl TEXT  Unfolded Studio API URL.  [default: https://api.unfolded.ai]
  --help          Show this message and exit.
```

### Python Package

The Python package can be imported via `unfolded.data_sdk`:

```py
from unfolded.data_sdk import DataSDK, ContentType

data_sdk = DataSDK(token='eyJ...')
```

#### List Datasets

List datasets for given user

```py
datasets = data_sdk.list_datasets()
```

#### Get Dataset by ID

Get dataset given its id

```py
dataset = datasets[0]
data_sdk.get_dataset_by_id(dataset)
```

#### Download dataset data

Download data for dataset given its id

```py
dataset = datasets[0]
data_sdk.download_dataset(dataset, output_file='output.csv')
```

#### Upload new dataset

Upload new dataset to Unfolded Studio

```py
data_sdk.upload_file(
    file='new_file.csv',
    name='Dataset name',
    content_type=ContentType.CSV,
    description='Dataset description')
```

#### Update existing dataset

Update data for existing Unfolded Studio dataset

```py
dataset = datasets[0]
data_sdk.update_dataset(
    file='new_file.csv',
    dataset=dataset,
    content_type=ContentType.CSV)
```

#### Delete dataset

Delete dataset from Unfolded Studio

**Warning: This operation cannot be undone.** If you delete a dataset
currently used in one or more maps, the dataset will be removed from
those maps, possibly causing them to render incorrectly.

```py
dataset = datasets[0]
data_sdk.delete_dataset(dataset)
```
