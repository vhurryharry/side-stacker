// utils/socket.ts
let socket: WebSocket | null = null

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws/game'

export const connectWebSocket = (gameId: string) => {
  if (socket) return

  const wsUrl = `${WS_URL}/${gameId}/`
  socket = new WebSocket(wsUrl)

  socket.onopen = () => console.log('WebSocket connected')
  socket.onclose = () => console.log('WebSocket disconnected')
  socket.onerror = (err) => console.error('WebSocket error', err)
}

export const isSocketConnected = () => {
  return socket && socket.readyState === WebSocket.OPEN
}

export const sendMessage = (data: any) => {
  if (socket && socket.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify(data))
  }
}

export const subscribeToMessages = (handler: (data: any) => void) => {
  if (socket) {
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data)
      handler(data)
    }
  }
}

export const disconnectWebSocket = () => {
  socket?.close()
  socket = null
}
