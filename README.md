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

## C++11 companion implementation

A separate portable C++ algorithm is available in [cpp/core.hpp](cpp/core.hpp), with [host tests](cpp/tests.cpp), [CMake](CMakeLists.txt) and [GitHub Actions](.github/workflows/cpp-core.yml). The Python implementation and its existing tests remain unchanged. See [C++ limitations and safety notes](cpp/README.md) for differences, embedded memory constraints and unverified Arduino/ESP32 hardware integration.
