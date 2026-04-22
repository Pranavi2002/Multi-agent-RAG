import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000";

export const queryRAG = async (question) => {
    const res = await axios.post(`${BASE_URL}/query`, {
        question
    });

    return res.data;
};

export const fetchHistory = async () => {
    const res = await axios.get(`${BASE_URL}/history`);
    return res.data;
};