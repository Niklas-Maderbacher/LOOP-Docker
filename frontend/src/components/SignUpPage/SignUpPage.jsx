// SignUpPage.jsx
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../LoginPage/LoginPage.modules.css';

function SignUpPage({ setIsAuthenticated }) {
    const [formData, setFormData] = useState({
        email: '',
        password: '',
        confirmPassword: '',
        displayName: ''
    });
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const validateForm = () => {
        if (!formData.email || !formData.password || !formData.confirmPassword || !formData.displayName) {
            setError('All fields are required');
            return false;
        }

        if (formData.password !== formData.confirmPassword) {
            setError('Passwords do not match');
            return false;
        }

        if (formData.password.length < 6) {
            setError('Password must be at least 6 characters long');
            return false;
        }

        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(formData.email)) {
            setError('Please enter a valid email address');
            return false;
        }

        return true;
    };

    const handleSignUp = async (event) => {
        event.preventDefault();
        setError(null);

        if (!validateForm()) {
            return;
        }

        setLoading(true);

        try {
            // Create new account
            const signUpResponse = await fetch('http://localhost:8000/api/v1/users/sign_up', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json' 
                },
                body: JSON.stringify({
                    email: formData.email,
                    password: formData.password,
                    display_name: formData.displayName
                })
            });

            if (!signUpResponse.ok) {
                const errorData = await signUpResponse.json();
                throw new Error(errorData.detail || 'Failed to create account');
            }

            // Automatically log in the user after successful sign-up
            const loginResponse = await fetch('http://localhost:8000/api/v1/security/token', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: new URLSearchParams({
                    username: formData.email,
                    password: formData.password
                })
            });

            if (!loginResponse.ok) {
                // Account created but login failed - redirect to login page
                alert('Account created successfully! Please log in.');
                navigate('/login');
                return;
            }

            const loginData = await loginResponse.json();
            localStorage.setItem('jwt', loginData.access_token);
            setIsAuthenticated(true);
            navigate('/');

        } catch (error) {
            setError(error.message);
        } finally {
            setLoading(false);
        }
    };

    const goToLogin = () => {
        navigate('/login');
    };

    return (
        <div className='content'>
            <h1>Create Account</h1>
            {error && <p className='error'>{error}</p>}
            <form onSubmit={handleSignUp}>
                <input 
                    type='text'
                    name='displayName'
                    placeholder='Full Name' 
                    value={formData.displayName} 
                    onChange={handleChange} 
                    required
                />
                <input 
                    type='email'
                    name='email' 
                    placeholder='Email' 
                    value={formData.email} 
                    onChange={handleChange} 
                    required
                />
                <input 
                    type='password'
                    name='password'
                    placeholder='Password' 
                    value={formData.password} 
                    onChange={handleChange} 
                    required
                />
                <input 
                    type='password'
                    name='confirmPassword'
                    placeholder='Confirm Password' 
                    value={formData.confirmPassword} 
                    onChange={handleChange} 
                    required
                />
                <button type='submit' disabled={loading}>
                    {loading ? 'Creating Account...' : 'Sign Up'}
                </button>
            </form>
            
            <div style={{ marginTop: '20px', textAlign: 'center' }}>
                <p>Already have an account?</p>
                <button 
                    type='button' 
                    onClick={goToLogin}
                    style={{
                        background: 'none',
                        border: 'none',
                        color: '#007bff',
                        cursor: 'pointer',
                        textDecoration: 'underline',
                        fontSize: '16px'
                    }}
                >
                    Sign In
                </button>
            </div>
        </div>
    );
}

export default SignUpPage;