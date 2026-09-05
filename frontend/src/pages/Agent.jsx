import { useState, useEffect, useRef } from 'react'

const API_BASE = 'https://shoppilot-ai-y3ci.onrender.com'

function Agent() {
  const [messages, setMessages] = useState([
    { role: 'agent', text: "Hi! I'm your AI Growth Agent. Ask me things like \"Why did my sales decrease?\" or \"Find abandoned carts.\"" }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  async function sendMessage() {
    if (!input.trim() || loading) return

    const userMessage = input
    setInput('')
    setMessages((prev) => [...prev, { role: 'user', text: userMessage }])
    setLoading(true)

    try {
      const res = await fetch(`${API_BASE}/api/agent/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage }),
      })
      const data = await res.json()

      setMessages((prev) => [
        ...prev,
        {
          role: 'agent',
          text: data.response,
          toolUsed: data.tool_used,
          actionTaken: data.action_taken,
        },
      ])
    } catch (err) {
      setMessages((prev) => [...prev, { role: 'agent', text: "Sorry, I couldn't reach the backend. Is it running?" }])
    } finally {
      setLoading(false)
    }
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter') sendMessage()
  }

  return (
    <div className="p-8 flex flex-col h-screen">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">AI Growth Agent</h2>

      <div className="flex-1 bg-white rounded-xl border border-gray-200 p-5 overflow-y-auto mb-4">
        {messages.map((msg, i) => (
          <div key={i} className={`mb-4 flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div
              className={`max-w-lg rounded-lg px-4 py-3 text-sm ${
                msg.role === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-800'
              }`}
            >
              <p>{msg.text}</p>
              {msg.toolUsed && (
                <p className="text-xs mt-2 opacity-60">Tool used: {msg.toolUsed}</p>
              )}
              {msg.actionTaken && (
                <div className="mt-2 pt-2 border-t border-gray-300 text-xs">
                  <p className="font-semibold">✓ Action taken:</p>
                  <p>{msg.actionTaken.name}</p>
                  <p className="opacity-70">Targeting {msg.actionTaken.target_customer_count} customers</p>
                </div>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start mb-4">
            <div className="bg-gray-100 text-gray-500 rounded-lg px-4 py-3 text-sm">
              Thinking...
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <div className="flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask about sales, abandoned carts, customers..."
          className="flex-1 border border-gray-300 rounded-lg px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          onClick={sendMessage}
          disabled={loading}
          className="bg-blue-600 text-white px-6 py-3 rounded-lg text-sm font-medium hover:bg-blue-700 disabled:opacity-50"
        >
          Send
        </button>
      </div>
    </div>
  )
}

export default Agent