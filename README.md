# Stream Window Engine

A Python standard-library CLI for aggregating timestamped JSONL events into fixed-duration (tumbling) time windows. Computes count, sum, mean, minimum and maximum per event group and window. Uses UTC timestamps and supports out-of-order input.

## Usage

```bash
python window_engine.py examples/events.jsonl
python window_engine.py examples/events.jsonl --window-seconds 30
```

Each JSONL event must have a timezone-aware ISO 8601 `timestamp` and finite numeric `value`, with optional string `group` (defaults to `default`).

## Tests

```bash
python -m unittest discover -s tests -v
```

Eight tests run on Python 3.10, 3.12 and 3.13 via GitHub Actions.

## Limitations

Despite the name, this is a **batch JSONL analyzer**, not a live distributed stream processor. It loads events into memory and does not support watermarks, late-event correction, event-time triggers, or backpressure.
