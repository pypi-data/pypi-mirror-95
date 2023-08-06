# QuarticSDK

Quartic SDK is Quartic.ai's external software development kit which allows users to use assets, tags, and other intelligence outside the Quartic AI Platform. Using the Quartic SDK, third party developers who have access to the Quartic AI Platform can build custom applications.

## Installation
---
Install using `pip`

```
pip install quartic-sdk
```
...or follow the following steps to install it from the source:
```
git clone https://github.com/Quarticai/QuarticSDK/
python setup.py install
```

## Example
---
Here's an example on how the Quartic SDK can be used:

#### Getting the assets, tags, batches from the server
```
# Assuming that the Quartic.ai server is at `https://test.quartic.ai/`, with the login
# and the username and password is `username` and `password.`

from quartic_sdk import APIClient

client = APIClient("https://test.quartic.ai/", username="username", password="password")
user_assets = client.assets() # Get the list of all assets that the user has access to

asset = user_assets.get(name="Test Asset") # Get a specific asset with the name "Test Asset"
asset_tags = asset.get_tags() # Gets the list of all tags

first_tag=asset_tags.first() # Returns the first in the list of tags
first_tag_data_iterator=first_tag.data(start_time=1000000,stop_time=2000000) # Returns the data present in the first tag for the time range of 1000000 to 2000000

```

## Documentation
---
To run the documentation locally, run the following in the terminal:
```
mkdocs serve
```

## Test Cases
---
To run the behaviour test cases, run the following:
```
aloe quartic_sdk/tests/
```
To run the unit test cases, run the following:
```
pytest
```
