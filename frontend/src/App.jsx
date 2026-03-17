import React, { useState } from 'react';
import axios from 'axios';
import ChatInterface from './components/ChatInterface';
import FileUploader from './components/FileUploader';
import { Cpu } from 'lucide-react';

function App() {
  const [messages, setMessages] = useState([]);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);

  // Use the backend URL (assuming FastAPI runs on 8000)
  const API_BASE = "http://localhost:8000";

  const handleUpload = async (file) => {
    setIsUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_BASE}/upload`, formData);
      setUploadedFile({ name: file.name, id: response.data.file_id });
      setMessages(prev => [...prev, { role: 'bot', content: `Uploaded **${file.name}**. I've analyzed the document. You can now ask questions about its content, including images and tables.` }]);
    } catch (error) {
      console.error("Upload failed", error);
      alert("Upload failed. Please check if the backend is running.");
    } finally {
      setIsUploading(false);
    }
  };

  const handleSendMessage = async (content) => {
    setMessages(prev => [...prev, { role: 'user', content }]);
    setIsProcessing(true);

    try {
      const response = await axios.post(`${API_BASE}/chat`, {
        message: content,
        file_id: uploadedFile?.id
      });
      setMessages(prev => [...prev, { 
        role: 'bot', 
        content: response.data.response,
        images: response.data.images 
      }]);
    } catch (error) {
      console.error("Chat failed", error);
      setMessages(prev => [...prev, { role: 'bot', content: "Sorry, I encountered an error while processing your request." }]);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <div style={{ background: 'var(--primary)', padding: '0.5rem', borderRadius: '10px' }}>
            <Cpu size={24} color="white" />
          </div>
          <h1 style={{ fontSize: '1.25rem', fontWeight: 800, letterSpacing: '-0.025em' }}>
            AGENTIC<span style={{ color: 'var(--primary)' }}>PDF</span>
          </h1>
        </div>
        <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
          Powered by Gemini 2.5 Flash
        </div>
      </header>

      <main className="main-content">
        <ChatInterface 
          messages={messages} 
          onSendMessage={handleSendMessage} 
          isProcessing={isProcessing} 
        />
        <FileUploader 
          onUpload={handleUpload} 
          isUploading={isUploading} 
          uploadedFile={uploadedFile} 
        />
      </main>
    </div>
  );
}

export default App;
