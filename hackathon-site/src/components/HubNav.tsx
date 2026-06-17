import { Link } from "react-router-dom";

const links = [
  { to: "/pattern", label: "The Pattern" },
  { to: "/intents", label: "The Six Doors" },
  { to: "/rules", label: "Rules" },
  { to: "/run-of-show", label: "Run of Show" },
  { to: "/runbook", label: "Student Runbook" },
];

export default function HubNav() {
  return (
    <nav className="flex flex-wrap justify-center gap-3 mt-10">
      {links.map((link) => (
        <Link
          key={link.to}
          to={link.to}
          className="px-5 py-2.5 rounded-xl bg-deep-cream text-maroon font-semibold text-sm hover:bg-deep-maroon hover:text-cream transition-colors shadow-sm"
        >
          {link.label}
        </Link>
      ))}
    </nav>
  );
}
