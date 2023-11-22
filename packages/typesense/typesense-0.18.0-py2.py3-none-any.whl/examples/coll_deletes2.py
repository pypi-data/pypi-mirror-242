import json
import random

with open('/home/kishore/Downloads/tsdata/hnstories_tiny.jsonl') as infile:
    lines = [line.rstrip() for line in infile]

    with open('/home/kishore/Downloads/tsdata/hnorder1.jsonl', 'w') as outfile1:
        i = 0
        for line in lines:
            obj = json.loads(line)
            obj['id'] = str(i)
            outfile1.write(json.dumps(obj) + '\n')
            i += 1

    random.shuffle(lines)

    with open('/home/kishore/Downloads/tsdata/hnorder2.jsonl', 'w') as outfile1:
        i = 0
        for line in lines:
            obj = json.loads(line)
            obj['id'] = str(i)
            outfile1.write(json.dumps(obj) + '\n')
            i += 1

