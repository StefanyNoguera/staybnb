import { NextPage } from 'next';
import { useState, ChangeEvent, FormEvent } from 'react';
import api from '../lib/api';

const Signup: NextPage = () => {
  const [form, setForm] = useState({ username: '', email: '', password: '' });
  const [message, setMessage] = useState<string>('');

  const handleChange = (e: ChangeEvent<HTMLInputElement>) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      await api.post('signup/', form);
      setMessage('Signup successful! Now log in.');
    } catch {
      setMessage('Signup failed. Try again.');
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10">
      <h1 className="text-2xl font-bold mb-4">Signup</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          name="username"
          onChange={handleChange}
          placeholder="Username"
          className="border p-2 w-full"
        />
        <input
          name="email"
          onChange={handleChange}
          placeholder="Email"
          className="border p-2 w-full"
        />
        <input
          name="password"
          onChange={handleChange}
          type="password"
          placeholder="Password"
          className="border p-2 w-full"
        />
        <button type="submit" className="bg-blue-500 text-white px-4 py-2">
          Sign Up
        </button>
      </form>
      {message && <p className="mt-4">{message}</p>}
    </div>
  );
};

export default Signup;
