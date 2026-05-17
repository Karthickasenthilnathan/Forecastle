import Sidebar from './Sidebar'
import Header from './Header'

export default function PageShell({ children, navItems, health, headerProps, title, subtitle }) {
  return (
    <div className="app-shell">
      <Sidebar navItems={navItems} health={health} />
      <main className="main-panel">
        {headerProps ? (
          <Header {...headerProps} />
        ) : (
          <header className="topbar">
            <div className="title-group">
              {subtitle && <p>{subtitle}</p>}
              <h1>{title || 'Forecastle'}</h1>
            </div>
          </header>
        )}
        {children}
      </main>
    </div>
  )
}
