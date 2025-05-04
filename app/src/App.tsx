import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import GameSetup from './pages/GameSetup'
import Game from './pages/Game'

function App() {
  return (
    <div className="w-full h-dvh flex flex-col items-center justify-start">
      <h1 className="h1">Side Stacker Game</h1>
      <Router>
        <Routes>
          <Route path="/" element={<GameSetup />} />
          <Route path="/game" element={<Game />} />
        </Routes>
      </Router>
    </div>
  )
}

export default App
