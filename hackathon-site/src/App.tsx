import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Landing from './pages/Landing';
import CardDetail from './pages/CardDetail';
import Pattern from './pages/Pattern';
import Intents from './pages/Intents';
import Rules from './pages/Rules';
import RunOfShow from './pages/RunOfShow';
import StudentRunbook from './pages/StudentRunbook';
import NotFound from './pages/NotFound';

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Landing />} />
        <Route path="/cards/:slug" element={<CardDetail />} />
        <Route path="/pattern" element={<Pattern />} />
        <Route path="/intents" element={<Intents />} />
        <Route path="/rules" element={<Rules />} />
        <Route path="/run-of-show" element={<RunOfShow />} />
        <Route path="/runbook" element={<StudentRunbook />} />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}
