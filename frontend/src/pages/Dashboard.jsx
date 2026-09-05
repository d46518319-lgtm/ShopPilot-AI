import { useState, useEffect } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
const API_BASE = 'https://shoppilot-ai-y3ci.onrender.com'

function StatCard({ label, value, sub }) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5">
      <p className="text-sm text-gray-500">{label}</p>
      <p className="text-2xl font-bold text-gray-800 mt-1">{value}</p>
      {sub && <p className="text-xs text-gray-400 mt-1">{sub}</p>}
    </div>
  )
}

function Dashboard() {
  const [stats, setStats] = useState(null)
  const [chartData, setChartData] = useState([])
  const [topProducts, setTopProducts] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchDashboardData() {
      try {
        const [statsRes, chartRes, productsRes] = await Promise.all([
          fetch(`${API_BASE}/api/dashboard/stats`),
          fetch(`${API_BASE}/api/dashboard/revenue-chart`),
          fetch(`${API_BASE}/api/dashboard/top-products`),
        ])
        setStats(await statsRes.json())
        setChartData(await chartRes.json())
        setTopProducts(await productsRes.json())
      } catch (err) {
        console.error('Failed to fetch dashboard data:', err)
      } finally {
        setLoading(false)
      }
    }
    fetchDashboardData()
  }, [])

  if (loading) {
    return <div className="p-8 text-gray-500">Loading dashboard...</div>
  }

  return (
    <div className="p-8">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Dashboard</h2>

      <div className="grid grid-cols-4 gap-4 mb-8">
        <StatCard label="Revenue" value={`₹${stats.revenue.toLocaleString()}`} sub="Last 7 days" />
        <StatCard label="Orders" value={stats.orders} sub="Last 7 days" />
        <StatCard label="Customers" value={stats.customers} sub="Total active" />
        <StatCard label="Conversion Rate" value={`${stats.conversion_rate}%`} sub="Last 7 days" />
      </div>

      <div className="bg-white rounded-xl border border-gray-200 p-5 mb-8">
        <h3 className="font-semibold text-gray-800 mb-4">Revenue (Last 7 Days)</h3>
        <ResponsiveContainer width="100%" height={250}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#eee" />
            <XAxis dataKey="day" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="revenue" stroke="#2563eb" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 p-5">
        <h3 className="font-semibold text-gray-800 mb-4">Top Products</h3>
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-gray-500 border-b">
              <th className="pb-2">Product</th>
              <th className="pb-2">Views</th>
              <th className="pb-2">Purchases</th>
              <th className="pb-2">Conversion</th>
            </tr>
          </thead>
          <tbody>
            {topProducts.map((p) => (
              <tr key={p.name} className="border-b last:border-0">
                <td className="py-3 font-medium text-gray-800">{p.name}</td>
                <td className="py-3 text-gray-600">{p.views.toLocaleString()}</td>
                <td className="py-3 text-gray-600">{p.purchases}</td>
                <td className="py-3 text-gray-600">{p.conversion}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default Dashboard