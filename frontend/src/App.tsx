import BriefingRoom from "./allclear/BriefingRoom";
import CloneGuide from "./allclear/CloneGuide";
import GlassBoxAudit from "./allclear/GlassBoxAudit";
import LiveCalls from "./allclear/LiveCalls";

export default function App() {
  const page = new URLSearchParams(window.location.search).get("page");
  if (page === "clone") return <CloneGuide />;
  if (page === "audit") return <GlassBoxAudit />;
  // Standalone demo surface: dial into the live phone line and project it on
  // its own URL/screen, decoupled from the main briefing room app.
  if (window.location.pathname === "/phone") {
    return <LiveCalls onExit={() => window.location.assign("/")} />;
  }
  return <BriefingRoom />;
}