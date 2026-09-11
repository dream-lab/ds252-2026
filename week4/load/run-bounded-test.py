"""
Bounded load generator — DS252 Week 4 fallback when JMeter is unavailable.
Hits /hash?rounds=<N> (CPU-intensive) for a fixed duration.

Usage:
  python load/run-bounded-test.py --url http://<ALB_DNS> --threads 20 --duration 180
"""
import argparse
import concurrent.futures
import time
import urllib.request
import urllib.error

def fetch(url, rounds, timeout=10):
    try:
        with urllib.request.urlopen(f"{url}/hash?rounds={rounds}", timeout=timeout) as r:
            t0 = time.monotonic()
            r.read()
            return r.status, round((time.monotonic() - t0) * 1000, 1)
    except Exception as e:
        return 0, str(e)[:60]

def worker(url, rounds, end_time, results):
    while time.time() < end_time:
        status, lat = fetch(url, rounds)
        if status == 200:
            results["ok"] += 1
            results["latencies"].append(lat)
        else:
            results["err"] += 1
        time.sleep(0.05)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--url",      required=True, help="Base URL, e.g. http://alb-dns")
    p.add_argument("--threads",  type=int, default=20)
    p.add_argument("--duration", type=int, default=180, help="Seconds")
    p.add_argument("--rounds",   type=int, default=10000, help="SHA-256 rounds per request")
    args = p.parse_args()

    url      = args.url.rstrip("/")
    end_time = time.time() + args.duration
    results  = {"ok": 0, "err": 0, "latencies": []}

    print(f"Starting bounded load: {args.threads} threads, {args.duration}s -> {url}/hash?rounds={args.rounds}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as pool:
        futs = [pool.submit(worker, url, args.rounds, end_time, results)
                for _ in range(args.threads)]
        while any(not f.done() for f in futs):
            remaining = max(0, end_time - time.time())
            print(f"\r  {remaining:.0f}s left  OK:{results['ok']}  ERR:{results['err']}",
                  end="", flush=True)
            time.sleep(5)

    lats = sorted(results["latencies"])
    n    = len(lats)
    print(f"\nResults ({args.duration}s):")
    print(f"  Total OK   : {results['ok']}")
    print(f"  Errors     : {results['err']}")
    if n:
        print(f"  p50 latency: {lats[int(n*0.50)]} ms")
        print(f"  p95 latency: {lats[int(n*0.95)]} ms")
        print(f"  p99 latency: {lats[min(int(n*0.99), n-1)]} ms")

if __name__ == "__main__":
    main()
