import './BaseLayout.css';

export function BaseLayout() {
  return (
    <div className="app-shell">
      <div className="app-shell__background">
        <div className="app-shell__scanlines" />
        <div className="app-shell__grid" />
        <div className="app-shell__glow" />
      </div>

      <div className="app-shell__frame">
        <header className="app-shell__header">
          <div className="app-shell__branding">
            <span className="app-shell__sigil">[MO]</span>
            <h1 className="app-shell__title">Mailopolis Control Room</h1>
          </div>
          <div className="app-shell__header-meta">
            <span className="app-shell__header-line">City Relay Terminal v0.1</span>
            <span className="app-shell__status-indicator">LINK GOOD</span>
          </div>
        </header>

        <div className="app-shell__body">
          <aside className="app-shell__dock app-shell__dock--left">
            <div className="dock-placeholder">Agent Directory Dock</div>
          </aside>

          <main className="app-shell__stage">
            <div className="stage__overlay">City Canvas Ready</div>
            <div className="stage__grid" />
            <div className="stage__horizon" />
          </main>

          <aside className="app-shell__dock app-shell__dock--right">
            <div className="dock-placeholder">City Dashboard Dock</div>
          </aside>
        </div>

        <footer className="app-shell__footer">
          <span className="footer__light" />
          <span className="footer__text">Awaiting system modules: Email, Dashboard, Contacts, Crisis Center</span>
        </footer>
      </div>
    </div>
  );
}
