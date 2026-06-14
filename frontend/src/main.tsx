import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import './index.css';
import { HomePage } from './pages/HomePage';
import { ResultsPage } from './pages/ResultsPage';
ReactDOM.createRoot(document.getElementById('root')!).render(<React.StrictMode><BrowserRouter><Routes><Route path="/" element={<HomePage/>}/><Route path="/results" element={<ResultsPage/>}/></Routes></BrowserRouter></React.StrictMode>);
