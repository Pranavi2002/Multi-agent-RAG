from time import time

class ObservabilityAgent:
    def log(self, query, retrieved_docs, eval_score, start_time):
        latency = round(time() - start_time, 2)
        print(f"\n[LOG]")
        print(f"Query: {query}")
        print(f"Retrieved Docs: {len(retrieved_docs)}")
        print(f"Eval Score: {eval_score}")
        print(f"Latency: {latency} sec\n")