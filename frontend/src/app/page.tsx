// src/app/page.tsx
'use client';

import { useEffect, useState } from 'react';
import api from '../lib/api';

type Property = {
  id: number;
  title: string;
  description: string;
  price_per_night: string;
  city: string;
  country: string;
};

export default function Home() {
  const [properties, setProperties] = useState<Property[]>([]);

  useEffect(() => {
    api.get<Property[]>('properties/')
      .then(res => setProperties(res.data))
      .catch(console.error);
  }, []);

  return (
    <div className="max-w-4xl mx-auto mt-10">
      <h1 className="text-3xl font-bold mb-6">Available Properties</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {properties.map(prop => (
          <div key={prop.id} className="border p-4 rounded">
            <h2 className="text-xl font-semibold">{prop.title}</h2>
            <p>{prop.description}</p>
            <p className="font-bold">${prop.price_per_night} / night</p>
            <p className="text-sm text-gray-500">{prop.city}, {prop.country}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
