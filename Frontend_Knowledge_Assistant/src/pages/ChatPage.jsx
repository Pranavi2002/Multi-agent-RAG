import { useState } from "react";
import { queryRAG } from "../api/ragApi";

import QueryBox from "../components/QueryBox";
import AnswerCard from "../components/AnswerCard";
import DocsPanel from "../components/DocsPanel";

export default function ChatPage() {
    const [answer, setAnswer] = useState("");
    const [docs, setDocs] = useState([]);
    const [metrics, setMetrics] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleQuery = async (question) => {
        setLoading(true);

        try {
            const res = await queryRAG(question);

            setAnswer(res.answer);
            setDocs(res.retrieved_docs);
            setMetrics(res.evaluation_score);
        } catch (err) {
            console.error(err);
        }

        setLoading(false);
    };

    return (
        <div>
            <h2>AI Knowledge Assistant</h2>

            <QueryBox onSubmit={handleQuery} loading={loading} />

            <AnswerCard answer={answer} metrics={metrics} />

            <DocsPanel docs={docs} />
        </div>
    );
}