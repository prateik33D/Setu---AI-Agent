import { useEffect, useRef, useState } from 'react'
import { useAuth } from '@clerk/clerk-react'

const WS_BASE_URL = (import.meta.env.VITE_WS_URL || 'ws://localhost:8000').replace(/^http/, 'ws')

export const useWebSocket = (userId) => {
  const { getToken, isSignedIn } = useAuth()
  const [connected, setConnected] = useState(false)
  const [messages, setMessages] = useState([])
  const [lastMessage, setLastMessage] = useState(null)
  const wsRef = useRef(null)
  const reconnectTimeoutRef = useRef(null)

  useEffect(() => {
    if (!isSignedIn || !userId) return

    const connect = async () => {
      try {
        const token = await getToken()
        const wsUrl = `${WS_BASE_URL}/ws/${userId}`
        const ws = new WebSocket(wsUrl)

        ws.onopen = () => {
          console.log('WebSocket connected')
          ws.send(JSON.stringify({ type: 'auth', token }))
          setConnected(true)
        }

        ws.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data)
            setLastMessage(data)
            setMessages((prev) => [...prev, data])
            if (data.type === 'connected') setConnected(true)
          } catch (e) {
            console.warn('WebSocket message parse error', e)
          }
        }

        ws.onerror = (error) => {
          console.error('WebSocket error:', error)
          setConnected(false)
        }

        ws.onclose = () => {
          console.log('WebSocket disconnected')
          setConnected(false)
          reconnectTimeoutRef.current = setTimeout(() => connect(), 3000)
        }

        wsRef.current = ws
      } catch (error) {
        console.error('Failed to connect WebSocket:', error)
      }
    }

    connect()

    return () => {
      if (wsRef.current) wsRef.current.close()
      if (reconnectTimeoutRef.current) clearTimeout(reconnectTimeoutRef.current)
    }
  }, [userId, isSignedIn, getToken])

  return { connected, messages, lastMessage }
}
