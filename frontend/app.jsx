const { useState, useEffect } = React;

const API_URL = "http://localhost:8000";

function App() {
    const [days, setDays] = useState([]);
    const [selectedDay, setSelectedDay] = useState(null);
    const [loading, setLoading] = useState(true);

    const [error, setError] = useState(null);

    const [mathAnswers, setMathAnswers] = useState({});

    useEffect(() => {
        fetch(`${API_URL}/days`)
            .then(res => {
                if (!res.ok) throw new Error("Failed to connect to backend");
                return res.json();
            })
            .then(data => {
                setDays(data);
                if (data.length > 0) {
                    setSelectedDay(data[0]);
                }
            })
            .catch(err => {
                console.error("Error fetching days:", err);
                setError(err.message);
            })
            .finally(() => setLoading(false));
    }, []);

    const handleDayChange = (e) => {
        const dayName = e.target.value;
        setLoading(true);
        // Reset math answers when day changes
        setMathAnswers({});
        fetch(`${API_URL}/days/${dayName}`)
            .then(res => res.json())
            .then(data => {
                setSelectedDay(data);
                setLoading(false);
            });
    };

    const handleMathAnswer = (id, value) => {
        setMathAnswers(prev => ({ ...prev, [id]: value }));
    };

    const checkMathAnswer = (prob) => {
        const userAnswer = mathAnswers[prob.id];
        if (!userAnswer) return null; // No input yet

        // Simple string comparison, assuming backend answer is string "5" etc.
        if (userAnswer.trim() === prob.answer) {
            return { color: '#2ECC71', status: '✅' }; // Correct
        } else {
            return { color: '#e74c3c', status: '❌' }; // Incorrect
            // Alternatively, don't show X, just neutral until right. 
            // But immediate feedback is good.
        }
    };

    if (error) return (
        <div className="container">
            <h1>⚠️ Oops!</h1>
            <p className="label-text" style={{ color: 'red' }}>{error}</p>
            <p>Please make sure the backend server is running.</p>
        </div>
    );

    if (!selectedDay) return <div className="container"><h1>Loading...</h1></div>;

    return (
        <div className="container">
            <h1>🦄 Liana's Kindergarten</h1>

            <div className="day-selector">
                <span className="label-text">Select Day:</span>
                <select value={selectedDay.name} onChange={handleDayChange}>
                    {days.map(day => (
                        <option key={day.id} value={day.name}>{day.name}</option>
                    ))}
                </select>
            </div>

            <div className="content-area">

                <div className="card">
                    <h2>📝 Sight Words</h2>
                    <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center' }}>
                        {selectedDay.tasks.map((task, index) => (
                            <div key={task.id} className="word-bubble">
                                <span className="word-number">{index + 1}</span>
                                <span className="word-text">{task.description}</span>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="card">
                    <h2>🧮 Math Fun</h2>
                    <div style={{ textAlign: 'center' }}>
                        {selectedDay.math_problems.map(prob => {
                            const feedback = checkMathAnswer(prob);
                            const borderColor = feedback ? feedback.color : '#ccc';

                            return (
                                <div key={prob.id} className="math-row">
                                    <span className="math-question">{prob.question}</span>
                                    <span className="math-equals">=</span>
                                    <input
                                        type="text"
                                        className="math-input"
                                        placeholder="?"
                                        value={mathAnswers[prob.id] || ''}
                                        onChange={(e) => handleMathAnswer(prob.id, e.target.value)}
                                        style={{ borderColor: borderColor, backgroundColor: feedback && feedback.status === '✅' ? '#d4edda' : 'white' }}
                                    />
                                    {feedback && <span className="math-feedback">{feedback.status}</span>}
                                </div>
                            );
                        })}
                    </div>
                </div>

                <div className="card">
                    <h2>✍️ Sentence Writing</h2>
                    {selectedDay.english_exercises.map(ex => (
                        <div key={ex.id}>
                            <div className="english-sentence">
                                "{ex.sentence}"
                            </div>
                        </div>
                    ))}
                </div>

            </div>
        </div>
    );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
