import { useEffect } from 'react'
import { Routes, Route } from 'react-router-dom'
import { ChartBarIcon, Cog6ToothIcon, CubeIcon, RadioIcon } from '@heroicons/react/24/outline'
import Dashboard from './pages/Dashboard'
import Products from './pages/Products'
import Signals from './pages/Signals'
import Settings from './pages/Settings'
import './App.css'

const navItems = [
  { label: 'Dashboard', icon: ChartBarIcon, path: '/' },
  { label: 'Products', icon: CubeIcon, path: '/products' },
  { label: 'Signals', icon: RadioIcon, path: '/signals' },
  { label: 'Settings', icon: Cog6ToothIcon, path: '/settings' },
]

function App() {
  useEffect(() => {
    document.title = 'Forecastle Demand Console'
  }, [])

  return (
    <Routes>
      <Route path="/" element={<Dashboard navItems={navItems} />} />
      <Route path="/products" element={<Products navItems={navItems} />} />
      <Route path="/signals" element={<Signals navItems={navItems} />} />
      <Route path="/settings" element={<Settings navItems={navItems} />} />
    </Routes>
  )
}

export default App
