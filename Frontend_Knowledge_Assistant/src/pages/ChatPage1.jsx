// no use of components

import { useState } from "react";
import { queryRAG } from "../api/ragApi";

export default function ChatPage() {
    const [question, setQuestion] = useState("");
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async () => {
        setLoading(true);

        try {
            const res = await queryRAG(question);
            setData(res);
        } catch (err) {
            console.error(err);
        }

        setLoading(false);
    };

    return (
        <div style={{ padding: "20px" }}>
            <h2>Multi-Agent RAG Chat</h2>

            <input
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Ask something..."
                style={{ width: "300px", padding: "8px" }}
            />

            <button onClick={handleSubmit}>
                Ask
            </button>

            {loading && <p>Loading...</p>}

            {data && (
                <div>
                    <h3>Answer</h3>
                    <p>{data.answer}</p>

                    <h4>Similarity Score</h4>
                    <pre>{JSON.stringify(data.evaluation_score, null, 2)}</pre>

                    <h4>Retrieved Docs</h4>
                    <ul>
                        {data.retrieved_docs.map((doc, i) => (
                            <li key={i}>
                                <p>{doc[0]}</p>
                                <small>Score: {doc[1]}</small>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}