import React, { useState } from 'react';
import axios from 'axios';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [userMessage, setUserMessage] = useState('');

  const handleMessageChange = (event) => {
    setUserMessage(event.target.value);
  };

  const handleSendMessage = async () => {
    if (userMessage.trim() === '') return;

    // Add user's message to the chat window
    setMessages([...messages, { text: userMessage, sender: 'You' }]);
    setUserMessage('');

    try {
      // Make a POST request to the Django API
      const response = await axios.post('http://127.0.0.1:8000/chat/api/chat/', {
        message: userMessage,
      });

      // Add the bot's response to the chat window
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: response.data.response, sender: 'Bot' },
      ]);
    } catch (error) {
      console.error("Error sending message:", error);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', fontFamily: 'Arial, sans-serif' }}>
      <div className="chat-box" 
           style={{
             width: '100%', maxWidth: '400px', height: '500px', border: '1px solid #ccc', 
             padding: '20px', overflowY: 'auto', borderRadius: '8px', backgroundColor: '#f9f9f9',
             boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)', marginBottom: '10px'}}>
        {messages.map((message, index) => (
          <div key={index} style={{ marginBottom: '15px' }}>
            <div style={{ fontWeight: 'bold', color: message.sender === 'You' ? '#007bff' : '#28a745' }}>
              {message.sender}:
            </div>
            <div style={{ fontSize: '14px', color: '#333', padding: '5px 10px', borderRadius: '8px', 
                         backgroundColor: message.sender === 'You' ? '#d1ecf1' : '#e2f7e3', 
                         maxWidth: '80%', wordBreak: 'break-word' }}>
              {message.text}
            </div>
          </div>
        ))}
      </div>

      <div style={{ display: 'flex', width: '100%', maxWidth: '400px', justifyContent: 'space-between' }}>
        <input
          type="text"
          value={userMessage}
          onChange={handleMessageChange}
          style={{
            width: '80%', padding: '10px', fontSize: '14px', borderRadius: '8px', border: '1px solid #ccc',
            outline: 'none', marginRight: '10px'}}
          placeholder="Type your message..."
        />
        <button 
          onClick={handleSendMessage}
          style={{
            width: '20%', backgroundColor: '#007bff', color: '#fff', border: 'none', borderRadius: '8px',
            padding: '10px', cursor: 'pointer', fontWeight: 'bold', transition: 'background-color 0.3s'}}
          onMouseOver={(e) => e.target.style.backgroundColor = '#0056b3'}
          onMouseOut={(e) => e.target.style.backgroundColor = '#007bff'}>
          Send
        </button>
      </div>
    </div>
  );
};

export default Chatbot;
