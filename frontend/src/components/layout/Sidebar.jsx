import { NavLink } from 'react-router-dom'
import { BoltIcon } from '@heroicons/react/24/solid'

export default function Sidebar({ navItems = [], health }) {
  return (
    <aside className="sidebar">
      <div className="brand-mark">
        <span className="brand-icon">
          <BoltIcon />
        </span>
        <div>
          <strong>Forecastle</strong>
          <small>Demand planning</small>
        </div>
      </div>

      <nav className="nav-list" aria-label="Main navigation">
        {navItems.map((item) => {
          const Icon = item.icon
          return (
            <NavLink
              className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}
              to={item.path}
              key={item.label}
              end={item.path === '/'}
            >
              <Icon />
              <span>{item.label}</span>
            </NavLink>
          )
        })}
      </nav>

      <div className="signal-pulse">
        <span className={health?.overall === 'healthy' ? 'pulse-dot' : 'pulse-dot warn'} />
        <div>
          <strong>{health?.overall === 'healthy' ? 'Signals live' : 'Signals degraded'}</strong>
          <small>{health?.sources?.length || 4} sources monitored</small>
        </div>
      </div>
    </aside>
  )
}
