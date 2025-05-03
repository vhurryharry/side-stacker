import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import SelectMode from './pages/SelectMode/SelectMode'
import Game from './pages/Game/Game'

function App() {
  return (
    <div className="app">
      <h1>Side Stacker Game</h1>
      <Router>
        <Routes>
          <Route path="/" element={<SelectMode />} />
          <Route path="/game" element={<Game />} />
        </Routes>
      </Router>
    </div>
  )
}

export default App
