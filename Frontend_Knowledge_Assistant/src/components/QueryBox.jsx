import { useState } from "react";

export default function QueryBox({ onSubmit, loading }) {
    const [text, setText] = useState("");

    const handleSubmit = () => {
        if (!text.trim()) return;
        onSubmit(text);
        setText("");
    };

    return (
        <div>
            <input
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Ask something..."
            />
            <button onClick={handleSubmit} disabled={loading}>
                {loading ? "Thinking..." : "Submit"}
            </button>
        </div>
    );
}