import { NavLink } from 'react-router-dom'

function Sidebar() {
  const linkClass = ({ isActive }) =>
    `block px-4 py-3 rounded-lg font-medium transition-colors ${
      isActive
        ? 'bg-blue-600 text-white'
        : 'text-gray-600 hover:bg-gray-100'
    }`

  return (
    <div className="w-64 h-screen bg-white border-r border-gray-200 flex flex-col p-4">
      <h1 className="text-xl font-bold text-gray-800 mb-8 px-2">
        ShopPilot AI
      </h1>
      <nav className="flex flex-col gap-2">
        <NavLink to="/" end className={linkClass}>
          Dashboard
        </NavLink>
        <NavLink to="/agent" className={linkClass}>
          AI Growth Agent
        </NavLink>
        <NavLink to="/campaigns" className={linkClass}>
          Campaigns
        </NavLink>
      </nav>
    </div>
  )
}

export default Sidebar