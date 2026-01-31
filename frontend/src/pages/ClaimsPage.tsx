import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Plus, Clock, DollarSign, FileText } from 'lucide-react'
import { claimsApi } from '../services/api'
import type { Claim } from '../types'
import Card from '../components/Card'
import Button from '../components/Button'
import Badge from '../components/Badge'

export default function ClaimsPage() {
  const [claims, setClaims] = useState<Claim[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // In a real app, this would come from authentication
  const userId = 'demo-user'

  useEffect(() => {
    loadClaims()
  }, [])

  const loadClaims = async () => {
    try {
      setLoading(true)
      const data = await claimsApi.getByUser(userId)
      setClaims(data)
    } catch (err) {
      setError('Failed to load claims')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    })
  }

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(amount)
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">My Claims</h1>
          <p className="text-gray-600 mt-1">
            View and manage all your insurance claims
          </p>
        </div>
        <Link to="/claims/new">
          <Button>
            <Plus className="w-4 h-4 mr-2" />
            New Claim
          </Button>
        </Link>
      </div>

      {/* Loading State */}
      {loading && (
        <Card>
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading claims...</p>
          </div>
        </Card>
      )}

      {/* Error State */}
      {error && (
        <Card className="border-red-200 bg-red-50">
          <p className="text-red-600">{error}</p>
        </Card>
      )}

      {/* Empty State */}
      {!loading && !error && claims.length === 0 && (
        <Card>
          <div className="text-center py-12">
            <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              No claims yet
            </h3>
            <p className="text-gray-600 mb-6">
              Get started by filing your first claim
            </p>
            <Link to="/claims/new">
              <Button>File a Claim</Button>
            </Link>
          </div>
        </Card>
      )}

      {/* Claims List */}
      {!loading && !error && claims.length > 0 && (
        <div className="space-y-4">
          {claims.map((claim) => (
            <Link key={claim.id} to={`/claims/${claim.id}`}>
              <Card className="hover:shadow-md transition-shadow cursor-pointer">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="text-lg font-semibold text-gray-900">
                        {claim.claim_number}
                      </h3>
                      <Badge status={claim.status} />
                    </div>

                    <p className="text-gray-600 mb-4">{claim.description}</p>

                    <div className="flex items-center gap-6 text-sm text-gray-500">
                      <span className="flex items-center gap-1">
                        <Clock className="w-4 h-4" />
                        {formatDate(claim.created_at)}
                      </span>
                      <span className="flex items-center gap-1">
                        <DollarSign className="w-4 h-4" />
                        {formatCurrency(claim.claim_amount)}
                      </span>
                      <span className="capitalize">
                        {claim.claim_type.replace('_', ' ')}
                      </span>
                    </div>

                    {claim.status_message && (
                      <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-md">
                        <p className="text-sm text-blue-800">
                          {claim.status_message}
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              </Card>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}
