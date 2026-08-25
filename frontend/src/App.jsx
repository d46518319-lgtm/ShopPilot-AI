import { Routes, Route } from 'react-router-dom'
import Sidebar from './components/Sidebar'
import Dashboard from './pages/Dashboard'
import Agent from './pages/Agent'
import Campaigns from './pages/Campaigns'

function App() {
  return (
    <div className="flex">
      <Sidebar />
      <div className="flex-1 bg-gray-50 min-h-screen">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/agent" element={<Agent />} />
          <Route path="/campaigns" element={<Campaigns />} />
        </Routes>
      </div>
    </div>
  )
}

export default App