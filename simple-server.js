// Simple Express server to test the project
import express from 'express';
import pg from 'pg';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const { Pool } = pg;

// Create a new pool
const pool = new Pool({ 
  connectionString: process.env.DATABASE_URL || 'postgres://postgres:postgres@localhost:5432/piata_ro'
});

const app = express();
const port = process.env.PORT || 3000;

// Serve static files from the client/dist directory
app.use(express.static(path.join(__dirname, 'client/dist')));

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

// Catch-all route to serve the frontend for any other routes
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'client/dist/index.html'));
});

// Start the server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
