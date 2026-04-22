import os
import pandas as pd
from pypdf import PdfReader

class DocumentFetcher:
    def __init__(self, folder_path="data", csv_path=None):
        self.folder_path = folder_path
        self.csv_path = csv_path

    def _read_pdf(self, path):
        reader = PdfReader(path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

    def fetch_documents(self):
        docs = []

        if os.path.exists(self.folder_path):
            for file in os.listdir(self.folder_path):
                path = os.path.join(self.folder_path, file)

                # TXT support
                if file.endswith(".txt"):
                    with open(path, "r", encoding="utf-8") as f:
                        docs.append(f.read())

                # PDF support
                elif file.endswith(".pdf"):
                    docs.append(self._read_pdf(path))

        # CSV support
        if self.csv_path and os.path.exists(self.csv_path):
            df = pd.read_csv(self.csv_path)
            docs.extend(df['content'].dropna().tolist())

        return docs