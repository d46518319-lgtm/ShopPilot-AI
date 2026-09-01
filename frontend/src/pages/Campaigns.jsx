import { useState, useEffect } from 'react'

const API_BASE = 'http://127.0.0.1:8000'

function Campaigns() {
  const [campaigns, setCampaigns] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchCampaigns() {
      try {
        const res = await fetch(`${API_BASE}/api/campaigns`)
        setCampaigns(await res.json())
      } catch (err) {
        console.error('Failed to fetch campaigns:', err)
      } finally {
        setLoading(false)
      }
    }
    fetchCampaigns()
  }, [])

  if (loading) {
    return <div className="p-8 text-gray-500">Loading campaigns...</div>
  }

  return (
    <div className="p-8">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Campaigns</h2>

      {campaigns.length === 0 && (
        <p className="text-gray-500">No campaigns yet. Ask the AI Growth Agent to find opportunities and it'll create some automatically.</p>
      )}

      <div className="grid gap-4">
        {campaigns.map((c) => (
          <div key={c.campaign_id} className="bg-white rounded-xl border border-gray-200 p-5">
            <div className="flex justify-between items-start mb-3">
              <div>
                <h3 className="font-semibold text-gray-800">{c.name}</h3>
                <p className="text-sm text-gray-500 mt-1">{c.target_description}</p>
              </div>
              <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full font-medium">
                {c.status}
              </span>
            </div>

            <p className="text-sm text-gray-700 mb-4">{c.offer_description}</p>

            {c.performance && (
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
                <p className="text-xs text-yellow-800 font-medium mb-2">
                  ⚠ {c.performance.simulation_note}
                </p>
                <div className="grid grid-cols-4 gap-3 text-center">
                  <div>
                    <p className="text-xs text-gray-500">Targeted</p>
                    <p className="font-bold text-gray-800">{c.performance.customers_targeted}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Converted</p>
                    <p className="font-bold text-gray-800">{c.performance.converted}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Revenue</p>
                    <p className="font-bold text-gray-800">₹{c.performance.revenue_generated.toLocaleString()}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">ROI</p>
                    <p className={`font-bold ${c.performance.roi_percent >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                      {c.performance.roi_percent}%
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

export default Campaigns
