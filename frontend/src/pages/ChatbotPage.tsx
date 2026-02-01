import { useState, useRef, useEffect, type KeyboardEvent } from 'react'
import { Send, Bot, User, Mic, MicOff } from 'lucide-react'
import { chatbotApi } from '../services/api'
import { useVoiceChat } from '../hooks/useVoiceChat'
import Card from '../components/Card'
import Button from '../components/Button'

interface Message {
  role: 'user' | 'assistant'
  content: string
  sources?: string[]
}

export default function ChatbotPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: "Hello! I'm your insurance assistant. I can help explain insurance terms, answer questions about the claims process, and guide you through your policy. What would you like to know?",
    },
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [sessionId] = useState(() => `session-${Date.now()}`)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const loadingRef = useRef(false)

  const appendMessage = (role: 'user' | 'assistant', content: string) => {
    setMessages((prev) => {
      const last = prev[prev.length - 1]
      if (last && last.role === role && last.content === content) {
        return prev
      }
      return [...prev, { role, content }]
    })
  }

  const sendMessage = async (messageText: string) => {
    const trimmed = messageText.trim()
    if (!trimmed || loadingRef.current) return

    setInput('')
    appendMessage('user', trimmed)

    try {
      loadingRef.current = true
      setLoading(true)
      const response = await chatbotApi.sendMessage(trimmed, sessionId)
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: response.response,
          sources: response.sources,
        },
      ])
    } catch (err) {
      console.error('Failed to send message:', err)
      appendMessage('assistant', 'Sorry, I encountered an error. Please try again.')
    } finally {
      loadingRef.current = false
      setLoading(false)
    }
  }

  const {
    status: voiceStatus,
    error: voiceError,
    start: startVoice,
    stop: stopVoice,
  } = useVoiceChat({
    sessionId,
    onTranscription: (role, text) => {
      if (role === 'user') {
        void sendMessage(text)
      } else {
        appendMessage(role, text)
      }
    },
  })

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    loadingRef.current = loading
  }, [loading])

  const handleSend = async () => {
    await sendMessage(input)
  }

  const handleKeyPress = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const suggestedQuestions = [
    "What is a deductible?",
    "How long does the claims process take?",
    "What documents do I need to submit?",
    "What does 'copay' mean?",
  ]

  const voiceActive = voiceStatus === 'ready' || voiceStatus === 'connecting'
  const voiceLabel =
    voiceStatus === 'ready'
      ? 'Listening'
      : voiceStatus === 'connecting'
      ? 'Connecting'
      : 'Off'

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Insurance Assistant</h1>
        <p className="text-gray-600 mt-1">
          Ask me anything about insurance terms, claims, or your policy
        </p>
      </div>

      <Card padding="none" className="flex flex-col" style={{ height: 'calc(100vh - 280px)' }}>
        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex gap-3 ${
                message.role === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              {message.role === 'assistant' && (
                <div className="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center flex-shrink-0">
                  <Bot className="w-5 h-5 text-primary-600" />
                </div>
              )}

              <div
                className={`max-w-[80%] rounded-lg px-4 py-3 ${
                  message.role === 'user'
                    ? 'bg-primary-600 text-white'
                    : 'bg-gray-100 text-gray-900'
                }`}
              >
                <p className="text-sm whitespace-pre-wrap">{message.content}</p>

                {message.sources && message.sources.length > 0 && (
                  <div className="mt-2 pt-2 border-t border-gray-300">
                    <p className="text-xs text-gray-600 mb-1">Sources:</p>
                    <div className="flex flex-wrap gap-1">
                      {message.sources.map((source, idx) => (
                        <span
                          key={idx}
                          className="inline-block px-2 py-0.5 bg-gray-200 rounded text-xs text-gray-700"
                        >
                          {source}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {message.role === 'user' && (
                <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center flex-shrink-0">
                  <User className="w-5 h-5 text-gray-600" />
                </div>
              )}
            </div>
          ))}

          {loading && (
            <div className="flex gap-3 justify-start">
              <div className="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center flex-shrink-0">
                <Bot className="w-5 h-5 text-primary-600" />
              </div>
              <div className="bg-gray-100 rounded-lg px-4 py-3">
                <div className="flex gap-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Suggested Questions (show only at start) */}
        {messages.length === 1 && (
          <div className="px-6 pb-4">
            <p className="text-sm text-gray-600 mb-2">Suggested questions:</p>
            <div className="flex flex-wrap gap-2">
              {suggestedQuestions.map((question, idx) => (
                <button
                  key={idx}
                  onClick={() => setInput(question)}
                  className="px-3 py-1.5 bg-gray-100 hover:bg-gray-200 rounded-full text-sm text-gray-700 transition-colors"
                >
                  {question}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Input */}
        <div className="border-t border-gray-200 p-4">
          <div className="flex items-center justify-between text-xs text-gray-500 mb-3">
            <div className="flex items-center gap-2">
              <span
                className={`inline-block w-2 h-2 rounded-full ${
                  voiceStatus === 'ready'
                    ? 'bg-emerald-500'
                    : voiceStatus === 'connecting'
                    ? 'bg-amber-500'
                    : 'bg-gray-300'
                }`}
              />
              <span>Voice: {voiceLabel}</span>
            </div>
            {voiceError && <span className="text-red-500">{voiceError}</span>}
          </div>
          <div className="flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask a question about insurance..."
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              disabled={loading}
            />
            <button
              onClick={voiceActive ? stopVoice : startVoice}
              className={`border rounded-lg px-3 py-2 transition-colors ${
                voiceActive
                  ? 'bg-emerald-500 text-white border-emerald-500 hover:bg-emerald-600'
                  : 'bg-white text-gray-600 border-gray-300 hover:bg-gray-100'
              }`}
              aria-label={voiceActive ? 'Stop voice' : 'Start voice'}
            >
              {voiceActive ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
            </button>
            <Button onClick={handleSend} disabled={!input.trim() || loading}>
              <Send className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </Card>
    </div>
  )
}
