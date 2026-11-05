import tempfile
import unittest
from pathlib import Path
from window_engine import aggregate,read_jsonl


def event(time,value=2,group="api"):
    return {"timestamp":"2026-11-05T10:00:"+time+"Z","value":value,"group":group}


class WindowTests(unittest.TestCase):
    def test_one_bucket(self):
        self.assertEqual(aggregate([event("00"),event("10")])[0]["count"],2)
    def test_mean(self):
        self.assertEqual(aggregate([event("00",2),event("10",4)])[0]["mean"],3)
    def test_grouping(self):
        self.assertEqual(len(aggregate([event("00"),event("00",3,"db")])),2)
    def test_window_boundary(self):
        self.assertEqual(len(aggregate([event("00"),event("30")],30)),2)
    def test_empty(self):
        self.assertEqual(aggregate([]),[])
    def test_bad_window(self):
        with self.assertRaises(ValueError): aggregate([],0)
    def test_bad_value(self):
        with self.assertRaises(ValueError): aggregate([event("00",float("nan"))])
    def test_jsonl(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/"events.jsonl"
            path.write_text('{"timestamp":"2026-11-05T10:00:00Z","value":2}\n',encoding="utf-8")
            self.assertEqual(len(read_jsonl(str(path))),1)


if __name__=="__main__":
    unittest.main()
