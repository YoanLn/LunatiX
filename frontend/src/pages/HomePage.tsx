import { Link } from 'react-router-dom'
import { FileText, Upload, MessageCircle, CheckCircle } from 'lucide-react'
import Card from '../components/Card'
import Button from '../components/Button'

export default function HomePage() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Hero Section */}
      <div className="text-center mb-16">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Simplify Your Insurance Claims
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          AI-powered platform to manage your insurance claims efficiently.
          Upload documents, track status, and get instant help.
        </p>
        <div className="mt-8 flex justify-center gap-4">
          <Link to="/claims/new">
            <Button size="lg">File a New Claim</Button>
          </Link>
          <Link to="/claims">
            <Button size="lg" variant="outline">View My Claims</Button>
          </Link>
        </div>
      </div>

      {/* Features */}
      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
        <Card>
          <FileText className="w-12 h-12 text-primary-600 mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            Easy Claim Filing
          </h3>
          <p className="text-gray-600 text-sm">
            Submit claims in minutes with our simple, guided process.
          </p>
        </Card>

        <Card>
          <Upload className="w-12 h-12 text-primary-600 mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            AI Document Verification
          </h3>
          <p className="text-gray-600 text-sm">
            Automatic verification of your documents using advanced AI technology.
          </p>
        </Card>

        <Card>
          <CheckCircle className="w-12 h-12 text-primary-600 mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            Real-Time Tracking
          </h3>
          <p className="text-gray-600 text-sm">
            Monitor your claim status and get updates at every step.
          </p>
        </Card>

        <Card>
          <MessageCircle className="w-12 h-12 text-primary-600 mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            24/7 AI Assistant
          </h3>
          <p className="text-gray-600 text-sm">
            Get instant answers to your insurance questions anytime.
          </p>
        </Card>
      </div>

      {/* How It Works */}
      <div className="mb-16">
        <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">
          How It Works
        </h2>
        <div className="grid md:grid-cols-3 gap-8">
          <div className="text-center">
            <div className="w-16 h-16 bg-primary-100 text-primary-600 rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
              1
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Submit Your Claim
            </h3>
            <p className="text-gray-600 text-sm">
              Provide claim details and upload required documents.
            </p>
          </div>

          <div className="text-center">
            <div className="w-16 h-16 bg-primary-100 text-primary-600 rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
              2
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              AI Verification
            </h3>
            <p className="text-gray-600 text-sm">
              Our AI instantly verifies your documents for completeness.
            </p>
          </div>

          <div className="text-center">
            <div className="w-16 h-16 bg-primary-100 text-primary-600 rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
              3
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Get Approved
            </h3>
            <p className="text-gray-600 text-sm">
              Track your claim and receive payment once approved.
            </p>
          </div>
        </div>
      </div>

      {/* CTA */}
      <Card className="bg-primary-50 border-primary-200">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Need Help Understanding Insurance Terms?
          </h2>
          <p className="text-gray-600 mb-4">
            Chat with our AI assistant to get instant explanations and answers.
          </p>
          <div className="flex items-center justify-center gap-2 text-primary-700">
            <MessageCircle className="w-5 h-5" />
            <p className="text-sm font-medium">
              Click the chat bubble in the bottom right corner to get started!
            </p>
          </div>
        </div>
      </Card>
    </div>
  )
}
