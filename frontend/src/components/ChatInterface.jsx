import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { Send, Bot, User } from 'lucide-react';

const ChatInterface = ({ messages, onSendMessage, isProcessing }) => {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim() && !isProcessing) {
      onSendMessage(input);
      setInput('');
    }
  };

  return (
    <div className="chat-section">
      <div className="messages-container">
        {messages.length === 0 && (
          <div style={{ textAlign: 'center', marginTop: '20%', opacity: 0.5 }}>
            <Bot size={64} style={{ marginBottom: '1rem' }} />
            <p>Upload a PDF and start chatting with the agent.</p>
          </div>
        )}
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
             <div style={{ display: 'flex', gap: '0.75rem', marginBottom: '0.25rem' }}>
                {msg.role === 'bot' ? <Bot size={16} /> : <User size={16} />}
                <span style={{ fontSize: '0.7rem', fontWeight: 'bold', textTransform: 'uppercase' }}>
                  {msg.role}
                </span>
             </div>
             <ReactMarkdown>{msg.content}</ReactMarkdown>
          </div>
        ))}
        {isProcessing && (
           <div className="message bot">
              <div className="typing-dots" style={{ display: 'flex', gap: '4px' }}>
                <span className="dot">.</span><span className="dot">.</span><span className="dot">.</span>
              </div>
           </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form className="input-area" onSubmit={handleSubmit}>
        <input 
          type="text" 
          className="chat-input" 
          placeholder="Ask a question about the document..." 
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={isProcessing}
        />
        <button type="submit" className="btn-primary" disabled={isProcessing || !input.trim()}>
          <Send size={20} />
        </button>
      </form>

      <style>{`
        .dot { animation: pulse 1.5s infinite; }
        .dot:nth-child(2) { animation-delay: 0.2s; }
        .dot:nth-child(3) { animation-delay: 0.4s; }
        @keyframes pulse { 0%, 100% { opacity: 0.3; } 50% { opacity: 1; } }
      `}</style>
    </div>
  );
};

export default ChatInterface;
