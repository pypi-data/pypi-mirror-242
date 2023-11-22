import random
import string
import time

import typesense


def random_string(n: int = 10) -> str:
    return "".join(random.choice(string.ascii_lowercase) for _ in range(n))


COLLECTION = "example"
client = typesense.Client(
    {
        "api_key": "abcd",
        "nodes": [{"host": "localhost", "port": "8108", "protocol": "http"}],
        "connection_timeout_seconds": 2,
    }
)

try:
    client.collections[COLLECTION].delete()
except:
    pass

n_documents = 10000
n_facet_fields = 30
n_values_per_facet_field = 30

facet_values = [random_string() for _ in range(n_values_per_facet_field)]


fields = [
    {
        "name": "title",
        "type": "string",
    },
    {
        "name": "grouping_id",
        "type": "string",
        "facet": True,
    },
]
for i in range(n_facet_fields):
    fields.append(
        {
            "name": f"facet{i}",
            "type": "string",
            "facet": True,
        }
    )


client.collections.create(
    {
        "name": COLLECTION,
        "fields": fields,
    }
)

documents = []
for i in range(n_documents):
    document = {
        "title": random_string(),
        "grouping_id": str(i % (n_documents // 4)),
    }
    for j in range(n_facet_fields):
        document[f"facet{j}"] = random.choice(facet_values)
    documents.append(document)

resp = client.collections[COLLECTION].documents.import_(documents, {"action": "create"})

for group_by in [True, False]:
    times_in_ms = []
    for _ in range(10):
        search_params = {
            "q": "*",
            "query_by": "title",
            "include_fields": "title,grouping_id",
            "facet_by": ",".join([f"facet{i}" for i in range(n_facet_fields)]),
            "max_facet_values": 100,
        }

        if group_by:
            search_params["group_by"] = "grouping_id"
            search_params["group_limit"] = 1

        start = time.perf_counter()
        hits = client.collections[COLLECTION].documents.search(search_params)
        end = time.perf_counter()
        time_in_ms = 1000 * (end - start)
        times_in_ms.append(time_in_ms)


    print(
        f"Mean time to search with {group_by=}: {sum(times_in_ms) / len(times_in_ms):.2f} ms"
    )