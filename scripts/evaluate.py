import os
import sys

eval_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "evaluation"))
sys.path.insert(0, eval_dir)

import evaluate
import asyncio

if __name__ == "__main__":
    asyncio.run(evaluate.run_evaluation())
