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
        } catch (error) {
            setError(error.message);
        }
    };

    const handleGoToSignUp = () => {
        navigate('/signup');
    };

    return (
        <div className='content'>
            <div className='login-card'>
                <h1>Login</h1>

                {error && <div className='error'>{error}</div>}

                <form className='login-form' onSubmit={handleLogin}>
                    <div className='form-group'>
                        <label className='form-label' htmlFor='email'>Email</label>
                        <input
                            id='email'
                            type='email'
                            placeholder='Enter your email'
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className='form-input'
                            required
                        />
                    </div>

                    <div className='form-group'>
                        <label className='form-label' htmlFor='password'>Password</label>
                        <input
                            id='password'
                            type='password'
                            placeholder='Enter your password'
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className='form-input'
                            required
                        />
                    </div>

                    <button type='submit' className='login-button'>
                        Login
                    </button>
                </form>

                <div className='signup-section'>
                    <p className='signup-text'>Don't have an account?</p>
                    <button
                        type='button'
                        onClick={handleGoToSignUp}
                        className='signup-button'
                    >
                        Sign Up
                    </button>
                </div>
            </div>
        </div>
    );
}

export default LoginPage;