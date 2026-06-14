import { useNavigate } from 'react-router-dom';
import { HeroSearch } from '../components/HeroSearch';
export function HomePage() { const navigate = useNavigate(); return <HeroSearch onSearch={(query) => navigate(`/results?q=${encodeURIComponent(query)}`)} />; }
