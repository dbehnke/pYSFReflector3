import threading
import time
import unittest
import sys
import os

# Ensure project root is on sys.path so tests can import the application module
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import importlib.util

# The project contains a script named 'YSFReflector' (no .py extension). Load it by path.
ysf_path = os.path.join(ROOT, 'YSFReflector')
with open(ysf_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the ClientLookup class block and extract it to avoid running module-level code
start = None
end = None
for i, line in enumerate(lines):
    if line.lstrip().startswith('class ClientLookup'):
        start = i
        break

if start is None:
    raise ImportError('ClientLookup class not found in YSFReflector')

# look for the next top-level class or EOF
for j in range(start + 1, len(lines)):
    if lines[j].startswith('class ') and not lines[j].startswith('class ClientLookup'):
        end = j
        break
if end is None:
    end = len(lines)

class_src = ''.join(lines[start:end])

# Prepare a minimal namespace with required imports used by the class
ns = {
    'threading': threading,
    'defaultdict': __import__('collections').defaultdict,
}

exec(compile(class_src, ysf_path, 'exec'), ns)
ClientLookup = ns.get('ClientLookup')
if ClientLookup is None:
    raise ImportError('ClientLookup not found after extraction')


class ConcurrentClientLookupTest(unittest.TestCase):
    def setUp(self):
        self.cl = ClientLookup()

    def _adder(self, start, count):
        for i in range(start, start + count):
            # client structure: [ip, port, call, ...]
            client = [f"127.0.0.{i}", 10000 + i, f"CALL{i}", None]
            self.cl.add_client(client)
            # small sleep to increase concurrency
            time.sleep(0.001)

    def _remover(self, start, count):
        for i in range(start, start + count):
            # Attempt to remove a matching client if present
            addr = f"127.0.0.{i}"
            port = 10000 + i
            c = self.cl.find_client(addr, port)
            if c:
                self.cl.remove_client(c)
            time.sleep(0.001)

    def _finder(self, start, count, results):
        for i in range(start, start + count):
            addr = f"127.0.0.{i}"
            port = 10000 + i
            c = self.cl.find_client(addr, port)
            if c:
                results.append((addr, port, c[2]))
            time.sleep(0.0005)

    def test_concurrent_add_remove_find(self):
        add_threads = []
        rem_threads = []
        find_threads = []
        results = []

        # Start several adders
        for t in range(5):
            thr = threading.Thread(target=self._adder, args=(t * 20, 20))
            thr.start()
            add_threads.append(thr)

        # Start finders concurrently
        for t in range(5):
            thr = threading.Thread(target=self._finder, args=(t * 20, 20, results))
            thr.start()
            find_threads.append(thr)

        # Start removers concurrently
        for t in range(5):
            thr = threading.Thread(target=self._remover, args=(t * 10, 10))
            thr.start()
            rem_threads.append(thr)

        # Wait for all threads to finish
        for thr in add_threads + find_threads + rem_threads:
            thr.join()

        # Verify internal consistency: all reported results actually map to clients
        for addr, port, call in results:
            c = self.cl.find_client(addr, port)
            # The client could have been removed by a concurrent remover; only assert
            # equality if the client is still present.
            if c is not None:
                self.assertEqual(c[2], call)

        # Perform a final integrity check: ensure client_map and clients list sizes are consistent
        # (client_map keys must point to valid indices)
        for key, idx in list(self.cl.client_map.items()):
            self.assertTrue(0 <= idx < len(self.cl.clients), f"stale index for {key}: {idx}")


if __name__ == '__main__':
    unittest.main()
