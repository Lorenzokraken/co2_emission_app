import React from 'react';
import CO2Dashboard from './components/CO2Dashboard';
import './App.css';

function App() {
  return (
    <div className="App">
      <div className="topbar">
        <h1>co2app</h1>
      </div>
      <CO2Dashboard />
    </div>
  );
}

export default App;