import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Landing from './pages/Landing';
import CardDetail from './pages/CardDetail';
import Pattern from './pages/Pattern';
import Intents from './pages/Intents';
import Rules from './pages/Rules';
import RunOfShow from './pages/RunOfShow';
import OperatorRunbook from './pages/OperatorRunbook';
import NotFound from './pages/NotFound';

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Landing />} />
        <Route path="/incidents/:slug" element={<CardDetail />} />
        <Route path="/workflow" element={<Pattern />} />
        <Route path="/queues" element={<Intents />} />
        <Route path="/policy" element={<Rules />} />
        <Route path="/shift-plan" element={<RunOfShow />} />
        <Route path="/runbook" element={<OperatorRunbook />} />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}
