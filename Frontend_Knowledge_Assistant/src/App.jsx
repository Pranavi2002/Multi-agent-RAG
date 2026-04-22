import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import ChatPage from "./pages/ChatPage";
import HistoryPage from "./pages/HistoryPage";

export default function App() {
    return (
        <BrowserRouter>
            <nav style={{ padding: "10px" }}>
                <Link to="/">Chat</Link> |{" "}
                <Link to="/history">History</Link>
            </nav>

            <Routes>
                <Route path="/" element={<ChatPage />} />
                <Route path="/history" element={<HistoryPage />} />
            </Routes>
        </BrowserRouter>
    );
}