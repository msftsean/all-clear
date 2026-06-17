import { Link } from "react-router-dom";

/**
 * Friendly 404 page rendered for unknown routes inside the shared Layout,
 * so the site header/footer chrome stays intact.
 */
export default function NotFound() {
  return (
    <div className="max-w-5xl mx-auto px-4 py-20 text-center">
      <p className="font-serif text-6xl font-bold text-deep-maroon">404</p>
      <h1 className="mt-4 font-serif text-3xl font-bold text-maroon">
        This door doesn&rsquo;t open
      </h1>
      <p className="mt-4 text-lg text-ink/70">
        We couldn&rsquo;t find the page you were looking for. Page not found.
      </p>
      <Link
        to="/"
        className="mt-8 inline-block rounded bg-deep-maroon px-6 py-3 text-base font-medium text-cream hover:bg-maroon focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gold transition-colors"
      >
        Back to the doors
      </Link>
    </div>
  );
}
