import { useEffect, useState } from "react";
import { fetchHistory } from "../api/ragApi";

export default function HistoryPage() {
    const [history, setHistory] = useState([]);

    useEffect(() => {
        loadHistory();
    }, []);

    const loadHistory = async () => {
        try {
            const data = await fetchHistory();
            setHistory(data);
        } catch (err) {
            console.error(err);
        }
    };

    return (
        <div>
            <h2>Query History</h2>

            <table border="1">
                <thead>
                    <tr>
                        <th>Question</th>
                        <th>Answer</th>
                        <th>Score</th>
                        <th>Latency</th>
                    </tr>
                </thead>

                <tbody>
                    {history.map((item) => (
                        <tr key={item.id}>
                            <td>{item.question}</td>
                            <td>{item.answer}</td>
                            <td>
                                <div>Avg Similarity: {item.avg_similarity}</div>
                                <div>Max Similarity: {item.max_similarity}</div>
                            </td>
                            <td>{item.latency}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}