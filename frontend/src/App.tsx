import BriefingRoom from "./allclear/BriefingRoom";
import CloneGuide from "./allclear/CloneGuide";

export default function App() {
  const page = new URLSearchParams(window.location.search).get("page");
  if (page === "clone") return <CloneGuide />;
  return <BriefingRoom />;
}