// no use of components

import { useEffect, useState } from "react";
import { fetchHistory } from "../api/ragApi";

export default function HistoryPage() {
    const [history, setHistory] = useState([]);

    useEffect(() => {
        loadHistory();
    }, []);

    const loadHistory = async () => {
        const res = await fetchHistory();
        setHistory(res);
    };

    return (
        <div style={{ padding: "20px" }}>
            <h2>Query History</h2>

            {history.map((item) => (
                <div key={item.id} style={{ border: "1px solid #ccc", margin: "10px", padding: "10px" }}>
                    <h4>Q: {item.question}</h4>
                    <p>{item.answer}</p>
                    <small>
                        Score: {item.avg_similarity} | Latency: {item.latency}s
                    </small>
                </div>
            ))}
        </div>
    );
}