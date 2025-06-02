// SignUpPage.jsx
// LOOP-104
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './SignUpPage.modules.css';

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
            <div className='signup-card'>
                <h1>Create Account</h1>

                {error && <div className='error'>{error}</div>}

                <form className='signup-form' onSubmit={handleSignUp}>
                    <div className='form-group'>
                        <label className='form-label' htmlFor='displayName'>Full Name</label>
                        <input
                            id='displayName'
                            type='text'
                            name='displayName'
                            placeholder='Enter your full name'
                            value={formData.displayName}
                            onChange={handleChange}
                            className='form-input'
                            required
                        />
                    </div>

                    <div className='form-group'>
                        <label className='form-label' htmlFor='email'>Email</label>
                        <input
                            id='email'
                            type='email'
                            name='email'
                            placeholder='Enter your email'
                            value={formData.email}
                            onChange={handleChange}
                            className='form-input'
                            required
                        />
                    </div>

                    <div className='form-group'>
                        <label className='form-label' htmlFor='password'>Password</label>
                        <input
                            id='password'
                            type='password'
                            name='password'
                            placeholder='Enter your password'
                            value={formData.password}
                            onChange={handleChange}
                            className='form-input'
                            required
                        />
                    </div>

                    <div className='form-group'>
                        <label className='form-label' htmlFor='confirmPassword'>Confirm Password</label>
                        <input
                            id='confirmPassword'
                            type='password'
                            name='confirmPassword'
                            placeholder='Confirm your password'
                            value={formData.confirmPassword}
                            onChange={handleChange}
                            className='form-input'
                            required
                        />
                    </div>

                    <button type='submit' className='signup-button' disabled={loading}>
                        {loading ? 'Creating Account...' : 'Create Account'}
                    </button>
                </form>

                <div className='login-section'>
                    <p className='login-text'>Already have an account?</p>
                    <button
                        type='button'
                        onClick={goToLogin}
                        className='login-link-button'
                    >
                        Sign In
                    </button>
                </div>
            </div>
        </div>
    );
}

export default SignUpPage;
