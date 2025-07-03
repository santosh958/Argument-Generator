import React, { useState, useEffect } from "react";
import axios from "axios";

const Upload = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [fileList, setFileList] = useState([]);
  const [argumentsResult, setArgumentsResult] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return setMessage("Please select a PDF file.");

    const formData = new FormData();
    formData.append("file", file);
    setMessage("Uploading...");

    try {
      const res = await axios.post("http://localhost:5000/upload", formData);
      setMessage(res.data.message);
      setFile(null);
      fetchFileList();
    } catch (error) {
      console.error(error);
      setMessage("❌ Upload failed.");
    }
  };

  const fetchFileList = async () => {
    try {
      const res = await axios.get("http://localhost:5000/list-files");
      setFileList(res.data.files);
    } catch (error) {
      console.error("Error fetching file list");
    }
  };

  const handleGenerateArguments = async (filename) => {
    setMessage("🔍 Generating arguments...");
    setArgumentsResult("");
    setLoading(true);

    try {
      const res = await axios.post("http://localhost:5000/generate", {
        filename: filename,
      });
      setArgumentsResult(res.data.result);
      setMessage("✅ Arguments generated.");
    } catch (error) {
      console.error(error);
      setMessage("❌ Failed to generate arguments.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFileList();
  }, []);

  return (
    <div style={styles.container}>
      <h1 style={styles.heading}>🎓 Research Paper Argument Generator</h1>

      <div style={styles.card}>
        <input type="file" accept="application/pdf" onChange={handleFileChange} />
        <button style={styles.button} onClick={handleUpload}>
          📤 Upload PDF
        </button>
        <p>{message}</p>
      </div>

      <div style={styles.card}>
        <h3>📁 Uploaded Files</h3>
        <ul style={styles.fileList}>
          {fileList.map((file, index) => (
            <li key={index} style={styles.fileItem}>
              <span>{file}</span>
              <button style={styles.genButton} onClick={() => handleGenerateArguments(file)}>
                ⚡ Generate Arguments
              </button>
            </li>
          ))}
        </ul>
      </div>

      {loading && <p style={{ textAlign: "center" }}>⏳ Processing...</p>}

      {argumentsResult && (
        <div style={styles.resultBox}>
          <h3>🧠 Extracted Arguments</h3>
          <pre style={styles.resultText}>{argumentsResult}</pre>
        </div>
      )}
    </div>
  );
};

const styles = {
  container: {
    maxWidth: "800px",
    margin: "0 auto",
    padding: "2rem",
    fontFamily: "Segoe UI, sans-serif",
  },
  heading: {
    textAlign: "center",
    marginBottom: "2rem",
    fontSize: "2rem",
    color: "#2b3a42",
  },
  card: {
    background: "#f9f9f9",
    borderRadius: "10px",
    padding: "1.5rem",
    marginBottom: "1.5rem",
    boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
  },
  button: {
    marginTop: "0.5rem",
    padding: "0.6rem 1.2rem",
    backgroundColor: "#007BFF",
    color: "#fff",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
  },
  fileList: {
    listStyle: "none",
    padding: 0,
  },
  fileItem: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "0.5rem 0",
    borderBottom: "1px solid #ddd",
  },
  genButton: {
    padding: "0.4rem 0.8rem",
    backgroundColor: "#28a745",
    color: "#fff",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
    fontSize: "0.9rem",
  },
  resultBox: {
    backgroundColor: "#fffef7",
    border: "1px solid #ddd",
    borderRadius: "10px",
    padding: "1.2rem",
    marginTop: "1.5rem",
  },
  resultText: {
    whiteSpace: "pre-wrap",
    fontFamily: "monospace",
    fontSize: "1rem",
    lineHeight: "1.6",
  },
};

export default Upload;

