// run-migrations.js
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import pg from 'pg';

const { Pool } = pg;

// Get the directory name of the current module
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load environment variables
const DATABASE_URL = process.env.DATABASE_URL || 'postgres://postgres:postgres@localhost:5432/piata_ro';

// Create a new pool
const pool = new Pool({ connectionString: DATABASE_URL });

/**
 * Runs all SQL migration files in the migrations directory
 */
async function runMigrations() {
  try {
    console.log('Running migrations...');
    
    // Create migrations table if it doesn't exist
    await pool.query(`
      CREATE TABLE IF NOT EXISTS migrations (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        applied_at TIMESTAMP NOT NULL DEFAULT NOW()
      )
    `);
    
    // Get all migration files
    const migrationsDir = path.resolve(__dirname, 'migrations');
    const migrationFiles = fs.readdirSync(migrationsDir)
      .filter(file => file.endsWith('.sql'))
      .sort(); // Sort to ensure migrations run in order
    
    // Get already applied migrations
    const { rows: appliedMigrations } = await pool.query('SELECT name FROM migrations');
    const appliedMigrationNames = appliedMigrations.map(m => m.name);
    
    // Run migrations that haven't been applied yet
    for (const file of migrationFiles) {
      if (!appliedMigrationNames.includes(file)) {
        console.log(`Applying migration: ${file}`);
        
        // Read and execute the migration file
        const filePath = path.join(migrationsDir, file);
        const sql = fs.readFileSync(filePath, 'utf8');
        
        // Start a transaction
        await pool.query('BEGIN');
        
        try {
          // Run the migration
          await pool.query(sql);
          
          // Record the migration
          await pool.query('INSERT INTO migrations (name) VALUES ($1)', [file]);
          
          // Commit the transaction
          await pool.query('COMMIT');
          
          console.log(`Migration ${file} applied successfully`);
        } catch (error) {
          // Rollback on error
          await pool.query('ROLLBACK');
          console.error(`Error applying migration ${file}:`, error);
          throw error;
        }
      }
    }
    
    console.log('Migrations completed');
  } catch (error) {
    console.error('Migration error:', error);
    throw error;
  } finally {
    // Close the pool
    await pool.end();
  }
}

// Run the migrations
runMigrations().catch(err => {
  console.error('Failed to run migrations:', err);
  process.exit(1);
});
