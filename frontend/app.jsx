import React from 'react';
import ResumeGenerator from './ResumeGenerator'; 
import './App.css'; 

const App = () => {
    return (
        <div className="App">
            <header className="App-header">
                <h1>Resume Generator</h1>
            </header>
            <main>
                <ResumeGenerator /> 
            </main>
        </div>
    );
};

export default App;
