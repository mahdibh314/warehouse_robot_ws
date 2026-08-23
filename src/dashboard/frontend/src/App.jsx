import { useState } from 'react'
import './App.css'

const API_URL = 'http://localhost:8000'

function App() {
  const [position, setPosition] = useState({ x: 0, y: 0 })

  const sendMove = async (linearX, angularZ) => {
    await fetch(`${API_URL}/move?linear_x=${linearX}&angular_z=${angularZ}`, {
      method: 'POST'
    })
  }

  const sendStop = async () => {
    await fetch(`${API_URL}/stop`, { method: 'POST' })
  }

  const refreshStatus = async () => {
    const response = await fetch(`${API_URL}/status`)
    const data = await response.json()
    setPosition(data.position)
  }

  return (
    <div>
      <h1>Warehouse Robot Dashboard</h1>

      <div>
        <button onClick={() => sendMove(0.3, 0.0)}>Avancer</button>
        <button onClick={() => sendMove(-0.3, 0.0)}>Reculer</button>
        <button onClick={() => sendMove(0.0, 0.5)}>Tourner gauche</button>
        <button onClick={() => sendMove(0.0, -0.5)}>Tourner droite</button>
        <button onClick={sendStop}>Stop</button>
      </div>

      <div>
        <button onClick={refreshStatus}>Rafraîchir position</button>
        <p>Position : x = {position.x.toFixed(2)}, y = {position.y.toFixed(2)}</p>
      </div>

      <div>
        <h2>Caméra en direct</h2>
        <img src={`${API_URL}/video_feed`} alt="Flux caméra du robot" width="640" />
      </div>

    </div>
  )
}

export default App
