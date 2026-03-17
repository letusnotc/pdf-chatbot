import React from 'react';
import { Upload, FileText, CheckCircle, AlertCircle } from 'lucide-react';
import { useDropzone } from 'react-dropzone';

const FileUploader = ({ onUpload, isUploading, uploadedFile }) => {
  const onDrop = (acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      onUpload(acceptedFiles[0]);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'application/pdf': ['.pdf'] },
    multiple: false
  });

  return (
    <div className="upload-section">
      <h2 style={{ marginBottom: '0.5rem' }}>PDF Context</h2>
      <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: '1.5rem' }}>
        Upload a document to enable multimodal agentic reasoning.
      </p>

      <div 
        {...getRootProps()} 
        className={`glass-card`}
        style={{ 
          borderStyle: 'dashed', 
          cursor: 'pointer',
          borderColor: isDragActive ? 'var(--primary)' : 'var(--glass-border)',
          textAlign: 'center',
          padding: '3rem 1rem'
        }}
      >
        <input {...getInputProps()} />
        <Upload size={40} color={isDragActive ? 'var(--primary)' : 'var(--text-muted)'} style={{ marginBottom: '1rem' }} />
        <p>{isDragActive ? "Drop the PDF here" : "Drag & drop PDF, or click to select"}</p>
      </div>

      {isUploading && (
        <div className="glass-card" style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div className="loader" style={{ width: '20px', height: '20px', border: '2px solid white', borderTopColor: 'transparent', borderRadius: '50%', animation: 'spin 1s linear infinite' }} />
          <span>Processing document...</span>
        </div>
      )}

      {uploadedFile && (
        <div className="glass-card" style={{ display: 'flex', alignItems: 'center', gap: '1rem', borderLeft: '4px solid #10b981' }}>
          <CheckCircle size={24} color="#10b981" />
          <div style={{ overflow: 'hidden' }}>
            <p style={{ fontWeight: 600 }}>{uploadedFile.name}</p>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Ready for chat</p>
          </div>
        </div>
      )}

      <style>{`
        @keyframes spin { to { transform: rotate(360deg); } }
      `}</style>
    </div>
  );
};

export default FileUploader;
