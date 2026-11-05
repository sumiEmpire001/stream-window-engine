"""Aggregate timestamped JSONL events into tumbling windows."""
import argparse
import collections
import datetime as dt
import json
import math


def timestamp(value):
    parsed=dt.datetime.fromisoformat(value.replace("Z","+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timezone required")
    return parsed.timestamp()


def aggregate(events,window_seconds=60):
    if not isinstance(window_seconds,int) or window_seconds<=0:
        raise ValueError("window_seconds must be a positive integer")
    buckets=collections.defaultdict(list)
    for event in events:
        if not isinstance(event,dict):
            raise ValueError("event must be an object")
        group=event.get("group","default")
        value=event.get("value")
        if not isinstance(group,str) or not group or isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value):
            raise ValueError("invalid event group or value")
        start=math.floor(timestamp(event["timestamp"])/window_seconds)*window_seconds
        buckets[(start,group)].append(value)
    result=[]
    for (start,group),values in sorted(buckets.items()):
        result.append({"window_start":dt.datetime.fromtimestamp(start,dt.timezone.utc).isoformat().replace("+00:00","Z"),
                       "group":group,"count":len(values),"sum":round(sum(values),5),
                       "mean":round(sum(values)/len(values),5),"min":min(values),"max":max(values)})
    return result


def read_jsonl(path):
    with open(path,encoding="utf-8") as source:
        return [json.loads(line) for line in source if line.strip()]


def main():
    parser=argparse.ArgumentParser(description="Tumbling window aggregation for JSONL events")
    parser.add_argument("file")
    parser.add_argument("--window-seconds",type=int,default=60)
    args=parser.parse_args()
    print(json.dumps(aggregate(read_jsonl(args.file),args.window_seconds),indent=2))


if __name__=="__main__":
    main()
