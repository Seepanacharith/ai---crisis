import asyncio
import os
import sys
import time
import numpy as np
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.rag.pipeline import rag_pipeline
from app.cache.redis_cache import disaster_cache

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("benchmark")

BENCHMARK_QUESTIONS = [
    ("What should I do during a flood?", "flood"),
    ("What should I keep in an emergency kit?", "emergency_kit"),
    ("What should I do during an earthquake?", "earthquake"),
    ("How should I evacuate during a fire?", "fire"),
    ("How do I prepare for a cyclone?", "cyclone"),
    ("What should I do if flood water is entering my house?", "flood"),
    ("What emergency supplies should I carry?", "emergency_kit"),
    ("How to perform CPR during an emergency?", "first_aid"),
    ("What is the Drop Cover Hold On technique?", "earthquake"),
    ("What should I do after a flood passes?", "flood"),
    ("How to handle a gas leak after an earthquake?", "earthquake"),
    ("What clothing should I wear during a wildfire evacuation?", "fire"),
    ("What is the eye of a cyclone?", "cyclone"),
    ("How much water per person per day is recommended?", "emergency_kit"),
    ("How to treat thermal burns on hands?", "first_aid"),
] * 4  # Expanded to 60 benchmark query runs

async def run_benchmark():
    print("\n=======================================================")
    print("      AI CRISIS COMPANION PERFORMANCE BENCHMARK       ")
    print("=======================================================\n")
    
    # Clear cache before benchmark run
    disaster_cache.clear()
    
    no_cache_latencies = []
    
    print("Phase 1: Measuring Cold Start / No-Cache Performance (60 Queries)...")
    for idx, (q, dtype) in enumerate(BENCHMARK_QUESTIONS):
        t0 = time.perf_counter()
        res = await rag_pipeline.execute(query=q, disaster_type=dtype, use_cache=False)
        t_ms = (time.perf_counter() - t0) * 1000
        no_cache_latencies.append(t_ms)
        if (idx + 1) % 15 == 0:
            print(f"  Processed {idx + 1}/60 queries... Current Avg: {np.mean(no_cache_latencies):.2f} ms")

    print("\nPhase 2: Measuring Warm Cache Performance (60 Repeated Queries)...")
    cached_latencies = []
    cache_hits = 0
    
    for idx, (q, dtype) in enumerate(BENCHMARK_QUESTIONS):
        t0 = time.perf_counter()
        res = await rag_pipeline.execute(query=q, disaster_type=dtype, use_cache=True)
        t_ms = (time.perf_counter() - t0) * 1000
        cached_latencies.append(t_ms)
        if res.get("cache_hit"):
            cache_hits += 1

    # Calculations
    before_avg = float(np.mean(no_cache_latencies))
    after_avg = float(np.mean(cached_latencies))
    
    before_p50 = float(np.percentile(no_cache_latencies, 50))
    after_p50 = float(np.percentile(cached_latencies, 50))
    
    before_p95 = float(np.percentile(no_cache_latencies, 95))
    after_p95 = float(np.percentile(cached_latencies, 95))
    
    hit_rate = (cache_hits / len(BENCHMARK_QUESTIONS)) * 100.0
    latency_reduction = ((before_avg - after_avg) / before_avg) * 100.0

    report = f"""
+-------------------------------------------------------------+
|               BENCHMARK PERFORMANCE METRICS                 |
+-------------------------------------------------------------+
                     Before (No Cache)     After (Cache Enabled)
Average Latency      {before_avg:8.2f} ms         {after_avg:8.2f} ms
P50 Latency          {before_p50:8.2f} ms         {after_p50:8.2f} ms
P95 Latency          {before_p95:8.2f} ms         {after_p95:8.2f} ms
Cache Hit Rate             0.0 %               {hit_rate:8.1f} %

---------------------------------------------------------------
Latency Reduction Improvement: {latency_reduction:.2f}% faster
Total Benchmark Queries Run:   {len(BENCHMARK_QUESTIONS)}
---------------------------------------------------------------
"""
    print(report)

if __name__ == "__main__":
    asyncio.run(run_benchmark())
