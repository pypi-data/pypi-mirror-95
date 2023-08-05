# MongoDB User Stores for Python

Python Store Implementation for Data Sets in MongoDB

1. [Usage](#usage)
2. [Methods](#methods)

## Usage

```python
from frappymongodataset import DataStore

MONGO_URL = "mongodb://localhost:27017"
data_set_store = DataStore(mongo_url=MONGO_URL, mongo_db="myDatabase", collection_name="dataSets")

all_data_sets = data_set_store.get_all()
specific_data_sets = data_set_store.get_by_assignment("primaryKey")
```

The return objects from `get` methods are objects of type `Data`. `Data` provides an attribute `payload`, which returns
the type of payload represented by the data set. These types are:

- `DataImagePayload` for images providing attributes `image_path`, `width` and `height`
- `DataJsonPayload` providing the JSON payload with the attribute `data`
- `DataTimeSeriesPayload` providing attributes `columns`, `data` (the rows), `date_format`, `index_column` and
 `column_mapping`

**Examples**

```python
from frappymongodataset import DataTypes

images = data_set_store.get_by_type(DataTypes.IMAGE)
print(images[0].payload.path, images[0].payload.dimensions["width"], images[0].payload.dimensions["height"])
# prints out something like: "_data/5e846d104e61db060094ed14.jpg 1200 600"
nd_array = images[0].to_np_array()  # will only work for IMAGE

time_series = data_set_store.get_by_type(DataTypes.TIME_SERIES)
print(time_series[0].payload.columns)
df = time_series[0].to_pd_data_frame()  # will only work for TIME_SERIES
```

## Methods

Base methods provided by [`pbu`](https://pypi.org/project/pbu/)

- `get_all()` - contrary to other stores, this will not return the payload of the individual data sets, but just the
 meta information
- `update_meta(data_id, meta_update)` - updating meta information, needs to contain "label" and "assignments" update
- `get_by_type(data_type)` - filters by the data sets `type` attribute
- `get_by_assignment_and_type(assignment_id, data_type)` - filters by the data sets `type` attribute and has to have an
 assignment for the group `assignment_id`
- `get_by_assignment(assignment_id)` - just checks for an `assignments` to the group provided
- `get_by_assignment_type(assignment_id, assignment_type)` - not to be confused with `get_by_assignment_and_type` - this
 method will check for the `assignment_id` in the `assignments`, and within that (a list of identifier) assignment for
 the type `assignment_type`
