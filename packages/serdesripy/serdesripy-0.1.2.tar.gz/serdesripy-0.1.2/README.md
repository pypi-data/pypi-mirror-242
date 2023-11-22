
`serdesripy` is a lightweight wrapper around
[`serde_esri`](https://github.com/JosiahParry/serde_esri) which is a
Rust library that can serialize and deserialize Esri JSON objects.

This python library is a proof of concept package illustrating how we
can call `serde_esri` to process JSON and return a PyArrow object.

Install from [PyPI](https://pypi.org/project/serdesripy/)

```python
import requests
import serdesripy

# make a simple request for US Counties boundaries
counties = requests.get("https://services.arcgis.com/P3ePLMYs2RVChkJx/ArcGIS/rest/services/USA_Counties_Generalized_Boundaries/FeatureServer/0/query?where=1%3D1&outFields=*&returnGeometry=true&resultRecordCount=10&f=json")

# pass in raw json and process the result
featureset = serdesripy.process_featureset(counties.text)
print(featureset)

# convert to pandas 
featureset.to_pandas()
```