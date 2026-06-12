import { Link, Outlet, useLocation } from 'react-router-dom';
import Footer from './Footer';
import MobileNav from './MobileNav';
import { HUB_LINKS } from '../data/nav';

export default function Layout() {
  const location = useLocation();
  const isHome = location.pathname === '/';

  return (
    <div className="min-h-screen flex flex-col">
      <a href="#main-content" className="skip-link">
        Skip to main content
      </a>

      {!isHome && (
        <header className="relative bg-cream border-b border-deep-cream">
          <div className="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between">
            <Link to="/" className="font-serif text-xl font-bold text-maroon hover:text-gold transition-colors">
              47 Doors
            </Link>
            <nav aria-label="Primary" className="hidden sm:flex gap-4 text-sm font-medium">
              {HUB_LINKS.map((link) => (
                <Link
                  key={link.to}
                  to={link.to}
                  className="text-ink/70 hover:text-maroon transition-colors"
                >
                  {link.label}
                </Link>
              ))}
            </nav>
            <MobileNav />
          </div>
        </header>
      )}

      <main id="main-content" tabIndex={-1} aria-label="Main content" className="flex-1 focus-visible:outline-none">
        <Outlet />
      </main>

      <Footer />
    </div>
  );
}
