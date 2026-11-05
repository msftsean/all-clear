import { Link } from "react-router-dom";

const links = [
  { to: "/workflow", label: "Triage workflow" },
  { to: "/queues", label: "Response queues" },
  { to: "/policy", label: "Severity & safety" },
  { to: "/shift-plan", label: "Shift plan" },
  { to: "/runbook", label: "Operator runbook" },
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
