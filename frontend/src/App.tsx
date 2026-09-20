import BriefingRoom from "./allclear/BriefingRoom";
import CloneGuide from "./allclear/CloneGuide";
import GlassBoxAudit from "./allclear/GlassBoxAudit";

export default function App() {
  const page = new URLSearchParams(window.location.search).get("page");
  if (page === "clone") return <CloneGuide />;
  if (page === "audit") return <GlassBoxAudit />;
  return <BriefingRoom />;
}