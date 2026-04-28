import { useState, useEffect, useRef } from "react";
import { FolderOpen, UploadCloud, File, X, Loader2 } from "lucide-react";

type DocumentType = {
  doc_id: string;
  source_name: string;
  chunks: number;
};

export function DocumentsPanel() {
  const [docs, setDocs] = useState<DocumentType[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const fetchDocs = async () => {
    try {
      const res = await fetch("/api/documents");
      const data = await res.json();
      setDocs(data.documents || []);
    } catch(err) {}
  };

  useEffect(() => {
    fetchDocs();
  }, []);

  const handleClear = async () => {
    await fetch("/api/documents", { method: "DELETE" });
    fetchDocs();
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsUploading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      await fetch("/api/documents/upload", {
        method: "POST",
        body: formData,
      });
      fetchDocs();
    } catch (err) {
      console.error(err);
    } finally {
      setIsUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = "";
    }
  };

  return (
    <div className="flex-1 p-6 overflow-y-auto max-w-[900px] mx-auto w-full">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-2">
          <h1 className="text-[20px] font-semibold text-[var(--text-primary)]">Documents</h1>
          <span className="bg-[var(--bg-elevated)] text-[var(--text-secondary)] text-[12px] px-2 py-0.5 rounded-full">{docs.length}</span>
        </div>
        <button onClick={handleClear} className="text-[13px] text-[var(--text-muted)] hover:text-[var(--color-error)]">Clear All</button>
      </div>

      <div 
        onClick={() => fileInputRef.current?.click()}
        className="border-2 border-dashed border-[var(--border-default)] rounded-[12px] p-8 text-center bg-[var(--bg-card)] hover:border-[var(--accent-primary)] hover:bg-[var(--accent-primary-dim)] transition-all cursor-pointer group mb-6"
      >
        <UploadCloud className="w-8 h-8 text-[var(--text-muted)] group-hover:text-[var(--accent-primary)] mx-auto mb-3 transition-colors" />
        <h3 className="text-[14px] font-medium text-[var(--text-secondary)] group-hover:text-[var(--accent-primary)]">
          {isUploading ? "Uploading..." : "Drop files here or click to upload"}
        </h3>
        <p className="text-[12px] text-[var(--text-muted)] mt-1">Supports PDF, TXT</p>
        <input 
          type="file" 
          ref={fileInputRef} 
          onChange={handleFileChange} 
          className="hidden" 
          accept=".pdf,.txt"
        />
      </div>

      {docs.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-10 text-center">
          <FolderOpen className="w-8 h-8 text-[var(--text-muted)] mb-3" />
          <h3 className="text-[16px] font-medium text-[var(--text-primary)]">No documents indexed</h3>
          <p className="text-[14px] text-[var(--text-secondary)] mt-1">Upload a PDF or text file to enable RAG-powered Q&A.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
          {docs.map((d, i) => (
            <div key={i} className="bg-[var(--bg-card)] border border-[var(--border-subtle)] rounded-[10px] p-3.5 flex flex-col group relative">
              <File className="w-6 h-6 text-[#e24b4a] mb-2" />
              <div className="text-[13px] font-medium text-[var(--text-primary)] truncate" title={d.source_name}>{d.source_name}</div>
              <div className="text-[11px] text-[var(--text-muted)] mt-1">{d.chunks} chunks indexed</div>
              <button className="absolute top-2 right-2 text-[var(--text-muted)] hover:text-[var(--color-error)] opacity-0 group-hover:opacity-100 transition-opacity">
                <X className="w-4 h-4" />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
