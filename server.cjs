// Simple Express server to test the project (CommonJS version)
const express = require('express');
const { Pool } = require('pg');
const path = require('path');
const cors = require('cors');

// Create a new pool
const pool = new Pool({ 
  connectionString: process.env.DATABASE_URL || 'postgres://postgres:postgres@localhost:5432/piata_ro'
});

const app = express();
const port = process.env.PORT || 5000;

// Enable CORS for the Vite frontend (running on port 5173)
app.use(cors({
  origin: 'http://localhost:5173',
  credentials: true
}));

// Parse JSON request body
app.use(express.json());

// API routes
app.get('/api/health', async (req, res) => {
  try {
    const result = await pool.query('SELECT NOW()');
    res.json({
      status: 'ok',
      timestamp: result.rows[0].now,
      env: process.env.NODE_ENV
    });
  } catch (error) {
    console.error('Database connection error:', error);
    res.status(500).json({
      status: 'error',
      message: 'Database connection failed',
      error: error.message
    });
  }
});

// Get all users
app.get('/api/users', async (req, res) => {
  try {
    const result = await pool.query('SELECT id, username, email, first_name, last_name, avatar, bio, location, is_admin, created_at, is_premium, is_verified FROM users');
    res.json({
      users: result.rows
    });
  } catch (error) {
    console.error('Error fetching users:', error);
    res.status(500).json({
      message: 'Error fetching users',
      error: error.message
    });
  }
});

// Get all categories
app.get('/api/categories', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM categories');
    res.json({
      categories: result.rows
    });
  } catch (error) {
    console.error('Error fetching categories:', error);
    res.status(500).json({
      message: 'Error fetching categories',
      error: error.message
    });
  }
});

// Get all listings
app.get('/api/listings', async (req, res) => {
  try {
    const result = await pool.query(`
      SELECT l.*, u.username, u.avatar, c.name as category_name, c.slug as category_slug
      FROM listings l
      JOIN users u ON l.user_id = u.id
      JOIN categories c ON l.category_id = c.id
      WHERE l.status = 'active'
      ORDER BY l.created_at DESC
      LIMIT 20
    `);
    res.json({
      listings: result.rows
    });
  } catch (error) {
    console.error('Error fetching listings:', error);
    res.status(500).json({
      message: 'Error fetching listings',
      error: error.message
    });
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
  console.log(`Vite frontend should be running at http://localhost:5173`);
});
