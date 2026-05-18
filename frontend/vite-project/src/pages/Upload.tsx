import { useRef, useState } from "react";
import api from "../services/api";

export default function Upload() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<string[]>([]);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a file");
      setSuccess("");
      return;
    }
    setError("");
    setSuccess("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await api.post("/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setResult(response.data.codes ?? []);
      setError("");
      setSuccess("Receipt sent. Receipt successfully uploaded.");
      setFile(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    } catch (err: any) {
      setSuccess("");
      if (err?.response?.status === 429) {
        setError("Too many requests. Please wait and try again.");
      } else {
        setError("Upload failed");
      }
    }
  };

  return (
    <div>
      <h1>Upload File</h1>

      <input
        type="file"
        ref={fileInputRef}
        onChange={(e) => setFile(e.target.files?.[0] ?? null)}
      />

      <button onClick={handleUpload}>
        Upload
      </button>

      {error ? <p>{error}</p> : null}
      {success ? <p>{success}</p> : null}

      {result.length ? (
        <ul>
          {result.map((code) => (
            <li key={code}>{code}</li>
          ))}
        </ul>
      ) : null}
    </div>
  );
}