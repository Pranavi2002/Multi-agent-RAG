# basic evaluation

class EvaluationAgent:
    def evaluate(self, query, answer):
        query_words = set(query.lower().split())
        answer_words = set(answer.lower().split())
        score = len(query_words & answer_words) / max(len(query_words), 1)
        return round(score, 2)   # 0 to 1