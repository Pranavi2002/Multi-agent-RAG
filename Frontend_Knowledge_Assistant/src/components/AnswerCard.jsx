export default function AnswerCard({ answer, metrics }) {
    if (!answer) return null;

    return (
        <div>
            <h3>Answer</h3>
            <p>{answer}</p>

            {metrics && (
                <div>
                    <p>Avg Similarity: {metrics.avg_similarity}</p>
                    <p>Max Similarity: {metrics.max_similarity}</p>
                    <p>Chunks Used: {metrics.num_chunks}</p>
                </div>
            )}
        </div>
    );
}