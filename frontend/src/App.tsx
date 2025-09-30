// import React, { useState, useRef, useEffect } from 'react';
// import axios from 'axios';

// // Define the structure for a chat message
// interface ChatMessage {
//   sender: 'user' | 'bot';
//   text: string;
// }

// // URL for your running FastAPI backend
// const API_URL = "http://127.0.0.1:8000/chat";

// function App() {
//   const [messages, setMessages] = useState<ChatMessage[]>([]);
//   const [inputValue, setInputValue] = useState<string>('');
//   const [isLoading, setIsLoading] = useState<boolean>(false);
//   const messagesEndRef = useRef<null | HTMLDivElement>(null);

//   // Automatically scroll to the latest message
//   const scrollToBottom = () => {
//     messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
//   };

//   useEffect(() => {
//     scrollToBottom();
//   }, [messages, isLoading]);

//   // Handle form submission
//   const handleSubmit = async (e: React.FormEvent) => {
//     e.preventDefault();
//     const userMessageText = inputValue.trim();
//     if (!userMessageText) return;

//     // 1. Add user's message to the chat optimistically
//     const userMessage: ChatMessage = { sender: 'user', text: userMessageText };
//     setMessages(prevMessages => [...prevMessages, userMessage]);
//     setInputValue('');
//     setIsLoading(true);

//     try {
//       // 2. Send message to the FastAPI backend
//       const response = await axios.post(API_URL, {
//         message: userMessageText,
//       });

//       // 3. Add the bot's response to the chat
//       const botMessage: ChatMessage = {
//         sender: 'bot',
//         text: response.data.response || "Sorry, I didn't get a response.",
//       };
//       setMessages(prevMessages => [...prevMessages, botMessage]);

//     } catch (error) {
//       console.error("Error fetching response:", error);
//       const errorMessage: ChatMessage = {
//         sender: 'bot',
//         text: "Oops! Something went wrong. Please try again.",
//       };
//       setMessages(prevMessages => [...prevMessages, errorMessage]);
//     } finally {
//       // 4. Stop the loading indicator
//       setIsLoading(false);
//     }
//   };

//   return (
//     <div className="flex flex-col h-screen bg-gray-100 font-sans">
//       <header className="bg-green-600 text-white p-4 text-center shadow-md">
//         <h1 className="text-2xl font-bold">Topia Farm AI 🧑‍🌾</h1>
//       </header>

//       <main className="flex-1 p-4 overflow-y-auto">
//         <div className="max-w-3xl mx-auto">
//           {/* Welcome Message */}
//           {messages.length === 0 && (
//             <div className="text-center p-6 bg-white rounded-lg shadow-sm">
//                 <p className="text-gray-600">
//                     Welcome to Topia Farm! Ask me to create a farm, buy/sell animals, or give you an investment plan.
//                 </p>
//             </div>
//           )}

//           {/* Chat Messages */}
//           {messages.map((msg, index) => (
//             <div key={index} className={`flex my-2 ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
//               <div
//                 className={`p-3 rounded-2xl max-w-lg shadow ${
//                   msg.sender === 'user'
//                     ? 'bg-green-500 text-white rounded-br-none'
//                     : 'bg-white text-gray-800 rounded-bl-none'
//                 }`}
//                 style={{ whiteSpace: 'pre-wrap' }} // This preserves newlines from the backend
//               >
//                 {msg.text}
//               </div>
//             </div>
//           ))}

//           {/* Loading Indicator */}
//           {isLoading && (
//             <div className="flex justify-start my-2">
//               <div className="p-3 rounded-2xl max-w-lg bg-white text-gray-800 rounded-bl-none shadow">
//                 <div className="flex items-center space-x-2">
//                   <span className="block w-2 h-2 bg-gray-400 rounded-full animate-pulse"></span>
//                   <span className="block w-2 h-2 bg-gray-400 rounded-full animate-pulse delay-75"></span>
//                   <span className="block w-2 h-2 bg-gray-400 rounded-full animate-pulse delay-150"></span>
//                 </div>
//               </div>
//             </div>
//           )}
          
//           {/* Invisible element to scroll to */}
//           <div ref={messagesEndRef} />
//         </div>
//       </main>

//       <footer className="bg-white p-4 border-t">
//         <form onSubmit={handleSubmit} className="max-w-3xl mx-auto flex items-center">
//           <input
//             type="text"
//             value={inputValue}
//             onChange={(e) => setInputValue(e.target.value)}
//             placeholder="Type your message..."
//             className="flex-1 p-3 border rounded-l-full focus:outline-none focus:ring-2 focus:ring-green-500"
//             disabled={isLoading}
//           />
//           <button
//             type="submit"
//             className="bg-green-600 text-white p-3 px-6 rounded-r-full hover:bg-green-700 disabled:bg-gray-400 transition-colors"
//             disabled={isLoading || !inputValue}
//           >
//             Send
//           </button>
//         </form>
//       </footer>
//     </div>
//   );
// }

// // export default App;
// import React, { useState, useRef, useEffect } from 'react';
// import axios from 'axios';

// // Define the structure for a chat message
// interface ChatMessage {
//   sender: 'user' | 'bot';
//   text: string;
// }

// // URL for your running FastAPI backend
// const API_URL = "http://127.0.0.1:8000/chat";

// // NEW HELPER FUNCTION: Checks if a string contains HTML tags.
// const isHtml = (text: string): boolean => {
//   const htmlRegex = /<([a-z][a-z0-9]*)\b[^>]*>/i;
//   return htmlRegex.test(text);
// };

// function App() {
//   const [messages, setMessages] = useState<ChatMessage[]>([]);
//   const [inputValue, setInputValue] = useState<string>('');
//   const [isLoading, setIsLoading] = useState<boolean>(false);
//   const messagesEndRef = useRef<null | HTMLDivElement>(null);

//   // Automatically scroll to the latest message
//   const scrollToBottom = () => {
//     messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
//   };

//   useEffect(() => {
//     scrollToBottom();
//   }, [messages, isLoading]);

//   // Handle form submission - NO CHANGES NEEDED HERE
//   const handleSubmit = async (e: React.FormEvent) => {
//     e.preventDefault();
//     const userMessageText = inputValue.trim();
//     if (!userMessageText) return;

//     const userMessage: ChatMessage = { sender: 'user', text: userMessageText };
//     setMessages(prevMessages => [...prevMessages, userMessage]);
//     setInputValue('');
//     setIsLoading(true);

//     try {
//       const response = await axios.post(API_URL, {
//         message: userMessageText,
//       });

//       const botMessage: ChatMessage = {
//         sender: 'bot',
//         text: response.data.response || "Sorry, I didn't get a response.",
//       };
//       setMessages(prevMessages => [...prevMessages, botMessage]);

//     } catch (error) {
//       console.error("Error fetching response:", error);
//       const errorMessage: ChatMessage = {
//         sender: 'bot',
//         text: "Oops! Something went wrong. Please try again.",
//       };
//       setMessages(prevMessages => [...prevMessages, errorMessage]);
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   return (
//     <div className="flex flex-col h-screen bg-gray-100 font-sans">
//       <header className="bg-green-600 text-white p-4 text-center shadow-md">
//         <h1 className="text-2xl font-bold">Topia Farm AI 🧑‍🌾</h1>
//       </header>

//       <main className="flex-1 p-4 overflow-y-auto">
//         <div className="max-w-3xl mx-auto">
//           {/* Welcome Message */}
//           {messages.length === 0 && (
//             <div className="text-center p-6 bg-white rounded-lg shadow-sm">
//               <p className="text-gray-600">
//                 Welcome to Topia Farm! Ask me to create a farm, buy/sell animals, or give you an investment plan.
//               </p>
//             </div>
//           )}

//           {/* Chat Messages */}
//           {messages.map((msg, index) => (
//             <div key={index} className={`flex my-2 ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
//               <div
//                 className={`p-3 rounded-2xl max-w-lg shadow ${
//                   msg.sender === 'user'
//                     ? 'bg-green-500 text-white rounded-br-none'
//                     : 'bg-white text-gray-800 rounded-bl-none'
//                 }`}
//                 style={{ whiteSpace: 'pre-wrap' }} // Preserves newlines for plain text
//               >
//                 {/* === UPDATED RENDERING LOGIC === */}
//                 {isHtml(msg.text) ? (
//                   // If it's HTML, render it directly.
//                   // Note: 'whiteSpace' style won't apply here; styling should be in the HTML string.
//                   <div dangerouslySetInnerHTML={{ __html: msg.text }} />
//                 ) : (
//                   // Otherwise, render as plain text.
//                   msg.text
//                 )}
//               </div>
//             </div>
//           ))}

//           {/* Loading Indicator */}
//           {isLoading && (
//             <div className="flex justify-start my-2">
//               <div className="p-3 rounded-2xl max-w-lg bg-white text-gray-800 rounded-bl-none shadow">
//                 <div className="flex items-center space-x-2">
//                   <span className="block w-2 h-2 bg-gray-400 rounded-full animate-pulse"></span>
//                   <span className="block w-2 h-2 bg-gray-400 rounded-full animate-pulse delay-75"></span>
//                   <span className="block w-2 h-2 bg-gray-400 rounded-full animate-pulse delay-150"></span>
//                 </div>
//               </div>
//             </div>
//           )}
          
//           {/* Invisible element to scroll to */}
//           <div ref={messagesEndRef} />
//         </div>
//       </main>

//       <footer className="bg-white p-4 border-t">
//         <form onSubmit={handleSubmit} className="max-w-3xl mx-auto flex items-center">
//           <input
//             type="text"
//             value={inputValue}
//             onChange={(e) => setInputValue(e.target.value)}
//             placeholder="Type your message..."
//             className="flex-1 p-3 border rounded-l-full focus:outline-none focus:ring-2 focus:ring-green-500"
//             disabled={isLoading}
//           />
//           <button
//             type="submit"
//             className="bg-green-600 text-white p-3 px-6 rounded-r-full hover:bg-green-700 disabled:bg-gray-400 transition-colors"
//             disabled={isLoading || !inputValue.trim()}
//           >
//             Send
//           </button>
//         </form>
//       </footer>
//     </div>
//   );
// }

// export default App;




import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { marked } from 'marked'; // Import the marked library

// Define the structure for a chat message
interface ChatMessage {
  sender: 'user' | 'bot';
  text: string;
}

// URL for your running FastAPI backend
const API_URL = "http://127.0.0.1:8000/chat";

// NEW HELPER FUNCTION: Detects if a string contains HTML OR a Markdown table
const containsHtmlOrMarkdownTable = (text: string): boolean => {
  // Regex to detect common HTML tags
  const htmlRegex = /<([a-z][a-z0-9]*)\b[^>]*>/i;
  // Regex to detect a markdown table structure (simplified)
  // Looks for lines with pipes '|' and a header separator '---'
  const markdownTableRegex = /\|.*\|[\r\n|\r|\n]+\| *:?-+:? *\|/m;
  return htmlRegex.test(text) || markdownTableRegex.test(text);
};


function App() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  // Automatically scroll to the latest message
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  // Handle form submission - NO CHANGES NEEDED HERE
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const userMessageText = inputValue.trim();
    if (!userMessageText) return;

    const userMessage: ChatMessage = { sender: 'user', text: userMessageText };
    setMessages(prevMessages => [...prevMessages, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await axios.post(API_URL, {
        message: userMessageText,
      });

      const botMessage: ChatMessage = {
        sender: 'bot',
        text: response.data.response || "Sorry, I didn't get a response.",
      };
      setMessages(prevMessages => [...prevMessages, botMessage]);

    } catch (error) {
      console.error("Error fetching response:", error);
      const errorMessage: ChatMessage = {
        sender: 'bot',
        text: "Oops! Something went wrong. Please try again.",
      };
      setMessages(prevMessages => [...prevMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100 font-sans">
      <header className="bg-green-600 text-white p-4 text-center shadow-md">
        <h1 className="text-2xl font-bold">Topia Farm AI 🧑‍🌾</h1>
      </header>

      <main className="flex-1 p-4 overflow-y-auto">
        <div className="max-w-3xl mx-auto">
          {/* Welcome Message */}
          {messages.length === 0 && (
            <div className="text-center p-6 bg-white rounded-lg shadow-sm">
              <p className="text-gray-600">
                Welcome to Topia Farm! Ask me to create a farm, buy/sell animals, or give you an investment plan.
              </p>
            </div>
          )}

          {/* Chat Messages */}
          {messages.map((msg, index) => (
            <div key={index} className={`flex my-2 ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div
                className={`p-3 rounded-2xl max-w-lg shadow ${
                  msg.sender === 'user'
                    ? 'bg-green-500 text-white rounded-br-none'
                    : 'bg-white text-gray-800 rounded-bl-none'
                }`}
                // IMPORTANT: Remove 'whiteSpace: pre-wrap' from here
                // We will handle newlines via Markdown conversion
              >
                {/* === UPDATED RENDERING LOGIC === */}
                {containsHtmlOrMarkdownTable(msg.text) ? (
                  // If it contains HTML or a Markdown table, convert it and render.
                  // marked.parse will convert Markdown tables (and other Markdown) to HTML.
                  <div dangerouslySetInnerHTML={{ __html: marked.parse(msg.text) }} />
                ) : (
                  // Otherwise, render as plain text.
                  msg.text
                )}
              </div>
            </div>
          ))}

          {/* Loading Indicator */}
          {isLoading && (
            <div className="flex justify-start my-2">
              <div className="p-3 rounded-2xl max-w-lg bg-white text-gray-800 rounded-bl-none shadow">
                <div className="flex items-center space-x-2">
                  <span className="block w-2 h-2 bg-gray-400 rounded-full animate-pulse"></span>
                  <span className="block w-2 h-2 bg-gray-400 rounded-full animate-pulse delay-75"></span>
                  <span className="block w-2 h-2 bg-gray-400 rounded-full animate-pulse delay-150"></span>
                </div>
              </div>
            </div>
          )}
          
          {/* Invisible element to scroll to */}
          <div ref={messagesEndRef} />
        </div>
      </main>

      <footer className="bg-white p-4 border-t">
        <form onSubmit={handleSubmit} className="max-w-3xl mx-auto flex items-center">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 p-3 border rounded-l-full focus:outline-none focus:ring-2 focus:ring-green-500"
            disabled={isLoading}
          />
          <button
            type="submit"
            className="bg-green-600 text-white p-3 px-6 rounded-r-full hover:bg-green-700 disabled:bg-gray-400 transition-colors"
            disabled={isLoading || !inputValue.trim()}
          >
            Send
          </button>
        </form>
      </footer>
    </div>
  );
}

export default App;

