import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import HomePage from './pages/HomePage'
import ClaimsPage from './pages/ClaimsPage'
import ClaimDetailPage from './pages/ClaimDetailPage'
import NewClaimPage from './pages/NewClaimPage'

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/claims" element={<ClaimsPage />} />
          <Route path="/claims/new" element={<NewClaimPage />} />
          <Route path="/claims/:id" element={<ClaimDetailPage />} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App
