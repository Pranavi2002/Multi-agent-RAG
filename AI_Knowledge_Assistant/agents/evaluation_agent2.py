# this will not work because
#  RAGAS, DeepEval internally uses an LLM to compute metrics like:
## faithfulness
## answer_relevancy
# By default, that LLM = OpenAI.
# So: ❌ No OpenAI key → RAGAS, DeepEval will always crash

from datasets import Dataset
from ragas import evaluate as ragas_evaluate
from ragas.metrics import faithfulness, answer_relevancy

from deepeval.metrics import AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase
from deepeval import evaluate as deepeval_evaluate


class EvaluationAgent:
    def evaluate(self, query, context_docs, answer):

        # -----------------------------
        # 1. FORMAT CONTEXT FOR RAGAS
        # -----------------------------
        ragas_contexts = [[doc for doc, _ in context_docs]]

        dataset = Dataset.from_dict({
            "question": [query],
            "answer": [answer],
            "contexts": ragas_contexts
        })

        # -----------------------------
        # 2. RAGAS EVALUATION (NO GT)
        # -----------------------------
        ragas_result = ragas_evaluate(
            dataset,
            metrics=[
                faithfulness,
                answer_relevancy
            ]
        )

        ragas_scores = ragas_result.to_pandas().to_dict()

        # -----------------------------
        # 3. DEEPEVAL EVALUATION
        # -----------------------------
        test_case = LLMTestCase(
            input=query,
            actual_output=answer,
            retrieval_context=[doc for doc, _ in context_docs]
        )

        deepeval_metric = AnswerRelevancyMetric()

        deepeval_result = deepeval_evaluate(
            test_cases=[test_case],
            metrics=[deepeval_metric]
        )

        # -----------------------------
        # 4. RETURN COMBINED SCORES
        # -----------------------------
        return {
            "ragas": ragas_scores,
            "deepeval": str(deepeval_result)
        }