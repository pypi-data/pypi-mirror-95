# Python MongoDB Content Store

Python Store Implementation for Content in MongoDB

## Usage

```python
from frappymongocontent import ContentStore

MONGO_URL = "mongodb://localhost:27017"
content_store = ContentStore(mongo_url=MONGO_URL, mongo_db="myDatabase", collection_name="content")
content_list = content_store.find_by_reference("my-demo")
for item in content_list:
    print(item.content, "is a dictionary with all the content")
```

## Methods

Base methods provided by [`pbu`](https://pypi.org/project/pbu/)

- `find_by_reference(references)` - retrieves content associated with the provided reference ID (e.g. `demo1`). This
 maps to the references declared by the embedding of the frontend module
 [`@frappy/react-content`](https://github.com/ilfrich/frappy-react-content)
- `find_by_reference_and_content_type(references, content_type)` - similar to `find_by_reference`, this additionally
 filters by content type as well. Content types are also declared by the embedding of the frontend module.
- `update_content(content_id, label, references, content)` - this is a complete update of the data (except for the
 content type, which shouldn't change with regular updates). This will completely replace a content objects label,
 reference assignment and the entire content (provided as `list` or `dict`, depending on the type of content (declared
 in the embedding of the frontend module)
