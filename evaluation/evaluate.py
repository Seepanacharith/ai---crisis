import asyncio
import json
import os
import sys
import time
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.rag.retriever import hybrid_retriever
from app.rag.pipeline import rag_pipeline

def calculate_word_overlap_score(str1: str, str2: str) -> float:
    words1 = set(str1.lower().split())
    words2 = set(str2.lower().split())
    if not words1 or not words2:
        return 0.0
    intersection = words1.intersection(words2)
    return len(intersection) / float(min(len(words1), len(words2)))

async def run_evaluation():
    print("\n=======================================================")
    print("           RAG ARCHITECTURE EVALUATION SUITE           ")
    print("=======================================================\n")
    
    eval_dir = os.path.dirname(__file__)
    questions_path = os.path.join(eval_dir, "questions.json")
    expected_path = os.path.join(eval_dir, "expected_answers.json")

    with open(questions_path, "r", encoding="utf-8") as f:
        questions = json.load(f)

    with open(expected_path, "r", encoding="utf-8") as f:
        expected_answers = json.load(f)

    retrieval_recalls = []
    context_relevances = []
    answer_relevances = []
    faithfulness_scores = []
    latencies = []

    print(f"Evaluating {len(questions)} crisis benchmark scenarios...\n")

    for item in questions:
        q_id = item["id"]
        query = item["question"]
        dtype = item.get("disaster_type", "all")
        expected = expected_answers.get(q_id, "")

        t0 = time.perf_counter()
        
        # 1. Measure Retrieval
        retrieved_chunks = hybrid_retriever.retrieve(query=query, disaster_type=dtype, top_k=10, rerank_top_k=4)
        
        # 2. Execute RAG
        rag_res = await rag_pipeline.execute(query=query, disaster_type=dtype, use_cache=False)
        total_time_ms = (time.perf_counter() - t0) * 1000
        latencies.append(total_time_ms)

        generated_answer = rag_res["response"]
        
        # Compute metrics
        # Retrieval recall: check if expected key terms appear in retrieved context
        context_text = " ".join([c["content"] for c in retrieved_chunks])
        recall = calculate_word_overlap_score(expected, context_text)
        retrieval_recalls.append(recall)

        # Context relevance
        context_rel = calculate_word_overlap_score(query, context_text)
        context_relevances.append(context_rel)

        # Answer relevance
        ans_rel = calculate_word_overlap_score(query, generated_answer)
        answer_relevances.append(ans_rel)

        # Faithfulness: answer vs context
        faithfulness = calculate_word_overlap_score(generated_answer, context_text)
        faithfulness_scores.append(faithfulness)

        print(f"[{q_id}] Query: '{query}' -> Latency: {total_time_ms:.1f}ms | Recall: {recall*100:.1f}%")

    avg_recall = np.mean(retrieval_recalls) * 100
    avg_context_rel = np.mean(context_relevances) * 100
    avg_ans_rel = np.mean(answer_relevances) * 100
    avg_faithfulness = np.mean(faithfulness_scores) * 100
    avg_latency = np.mean(latencies)

    report = f"""
+-------------------------------------------------------------+
|                 RAG EVALUATION METRICS REPORT               |
+-------------------------------------------------------------+
  Retrieval Recall:     {avg_recall:6.2f} %
  Context Relevance:    {avg_context_rel:6.2f} %
  Answer Relevance:     {avg_ans_rel:6.2f} %
  Faithfulness:         {avg_faithfulness:6.2f} %
  Average Latency:      {avg_latency:6.2f} ms
+-------------------------------------------------------------+
"""
    print(report)

    output_report_path = os.path.join(eval_dir, "eval_results.json")
    with open(output_report_path, "w", encoding="utf-8") as f:
        json.dump({
            "retrieval_recall_pct": round(avg_recall, 2),
            "context_relevance_pct": round(avg_context_rel, 2),
            "answer_relevance_pct": round(avg_ans_rel, 2),
            "faithfulness_pct": round(avg_faithfulness, 2),
            "average_latency_ms": round(avg_latency, 2)
        }, f, indent=2)

if __name__ == "__main__":
    asyncio.run(run_evaluation())
