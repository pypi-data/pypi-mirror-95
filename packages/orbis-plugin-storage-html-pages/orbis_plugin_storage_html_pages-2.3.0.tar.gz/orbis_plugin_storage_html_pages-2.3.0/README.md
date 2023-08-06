# HTML Pages Storage Plugin for Orbis

This plugin generates an HTML web page for each gold document with the corresponding results of the service.

![screenshot](screenshot.png)

## Show clustering

In order for the clusters to be displayed, the following element must be added to all dictionaries in the array returned
in the aggregation step in the ```map_entities``` function.

```python
from orbis_eval.core.base import AggregationBaseClass

class MyAggregation(AggregationBaseClass):

    def map_entities(self, response, item):
        result = []
        cluster_name = "name of cluster"
        result.append({
                ...,
                "annotations": [{"type": "Cluster", "entity": cluster_name}]
            })
        return result
```