const { Client } = require('pg');

// Create a new client
const client = new Client({
  connectionString: 'postgres://postgres:postgres@localhost:5432/piata_ro'
});

async function testConnection() {
  try {
    // Connect to the database
    await client.connect();
    console.log('Connected to the database');

    // Test query
    const result = await client.query('SELECT NOW()');
    console.log('Database time:', result.rows[0].now);

    // Check if tables exist
    const tablesResult = await client.query(`
      SELECT table_name 
      FROM information_schema.tables 
      WHERE table_schema = 'public'
    `);
    
    console.log('Tables in the database:');
    tablesResult.rows.forEach(row => {
      console.log(`- ${row.table_name}`);
    });

    // Close the connection
    await client.end();
    console.log('Connection closed');
  } catch (error) {
    console.error('Error:', error);
  }
}

// Run the test
testConnection();
