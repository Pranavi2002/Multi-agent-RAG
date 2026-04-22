export default function DocsPanel({ docs }) {
    if (!docs || docs.length === 0) return null;

    return (
        <div>
            <h3>Retrieved Documents</h3>
            <ul>
                {docs.map((doc, idx) => (
                    <li key={idx}>
                        <p>{doc[0]}</p>
                        <small>Score: {doc[1]}</small>
                    </li>
                ))}
            </ul>
        </div>
    );
}