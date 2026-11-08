import BriefingRoom from "./allclear/BriefingRoom";
import CloneGuide from "./allclear/CloneGuide";
import GlassBoxAudit from "./allclear/GlassBoxAudit";
import LiveCalls from "./allclear/LiveCalls";
import SurgeBoard from "./allclear/surge/SurgeBoard";
import SurgeCards from "./allclear/surge/SurgeCards";
import SurgeReport from "./allclear/surge/SurgeReport";

export default function App() {
  const page = new URLSearchParams(window.location.search).get("page");
  if (page === "clone") return <CloneGuide />;
  if (page === "audit") return <GlassBoxAudit />;
  // Standalone demo surface: dial into the live phone line and project it on
  // its own URL/screen, decoupled from the main briefing room app.
  if (window.location.pathname === "/phone") {
    return <LiveCalls onExit={() => window.location.assign("/")} />;
  }
  // Room surge (024): audience reports from phones, the room display shows the
  // collapse, and printable table cards carry per-scenario QR codes.
  const path = window.location.pathname.replace(/\/+$/, "");
  if (path === "/report") return <SurgeReport />;
  if (path === "/surge") return <SurgeBoard />;
  if (path === "/surge/cards") return <SurgeCards />;
  return <BriefingRoom />;
}