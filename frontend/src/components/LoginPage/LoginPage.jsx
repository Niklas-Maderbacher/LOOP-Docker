// LOOP-115 Thomas Sommerauer
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './LoginPage.modules.css';

function LoginPage({ setIsAuthenticated }) {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleLogin = async (event) => {
        event.preventDefault();
        setError(null);
        
        try {
            const response = await fetch('http://localhost:8000/api/v1/security/token', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: new URLSearchParams({
                    username: email,
                    password: password
                })
            });

            if (!response.ok) {
                throw new Error('Invalid email or password');
            }
            
            const data = await response.json();
            localStorage.setItem('jwt', data.access_token);
            setIsAuthenticated(true);
            navigate('/');
        } catch (error) {
            setError(error.message);
        }
    };

    const handleGoToSignUp = () => {
        navigate('/signup');
    };

    return (
        <div className='content'>
            <h1>Login Page</h1>
            {error && <p className='error'>{error}</p>}
            <form onSubmit={handleLogin}>
                <input 
                    type='email' 
                    placeholder='Email' 
                    value={email} 
                    onChange={(e) => setEmail(e.target.value)} 
                    required
                />
                <input 
                    type='password' 
                    placeholder='Password' 
                    value={password} 
                    onChange={(e) => setPassword(e.target.value)} 
                    required
                />
                <button type='submit'>Login</button>
            </form>

            <div style={{ marginTop: '20px', textAlign: 'center' }}>
                <p>Don't have an account?</p>
                <button 
                    type='button' 
                    onClick={handleGoToSignUp}
                    style={{
                        background: '#28a745',
                        color: 'white',
                        border: 'none',
                        padding: '10px 20px',
                        borderRadius: '4px',
                        cursor: 'pointer',
                        fontSize: '16px'
                    }}
                >
                    Sign Up
                </button>
            </div>
        </div>
    );
}

export default LoginPage;