// Express server for the marketplace app
const express = require('express');
const { Pool } = require('pg');
const path = require('path');
const fs = require('fs');

// Create a new pool
const pool = new Pool({
  connectionString: process.env.DATABASE_URL || 'postgres://postgres:postgres@localhost:5432/piata_ro'
});

const app = express();
const port = process.env.PORT || 3000;

// Serve static files
app.use(express.static('public'));

// Set up template engine
app.set('view engine', 'html');
app.engine('html', function(filePath, options, callback) {
  fs.readFile(filePath, function(err, content) {
    if (err) return callback(err);

    // Replace template variables
    let rendered = content.toString();

    if (options.categories) {
      let categoryOptions = '';
      options.categories.forEach(category => {
        categoryOptions += `<option value="${category.id}">${category.name}</option>`;
      });
      rendered = rendered.replace('{% for category in categories %}\n                            <option value="{{ category.id }}">{{ category.name }}</option>\n                            {% endfor %}', categoryOptions);
    }

    if (options.featured_listings) {
      let featuredListingsHtml = '';
      if (options.featured_listings.length > 0) {
        options.featured_listings.forEach(listing => {
          featuredListingsHtml += `
            <div class="col-md-3 mb-4">
                <div class="listing-card">
                    ${listing.images && listing.images.length > 0
                      ? `<img src="${listing.images[0]}" alt="${listing.title}" class="listing-img">`
                      : `<div class="listing-img bg-light d-flex align-items-center justify-content-center">
                          <i class="fas fa-image text-secondary" style="font-size: 3rem;"></i>
                         </div>`
                    }
                    <div class="card-body">
                        <h5 class="card-title text-truncate">${listing.title}</h5>
                        <p class="listing-price">${listing.price} ${listing.currency}</p>
                        <p class="listing-location"><i class="fas fa-map-marker-alt me-1"></i> ${listing.location}</p>
                        <p class="card-text text-muted small">${new Date(listing.created_at).toLocaleDateString('ro-RO')}</p>
                        <a href="/listings/${listing.id}" class="btn btn-sm btn-outline-primary w-100">Vezi detalii</a>
                    </div>
                </div>
            </div>
          `;
        });
      } else {
        featuredListingsHtml = `
          <div class="col-12 text-center py-5">
              <p class="text-muted">Nu există anunțuri promovate momentan.</p>
          </div>
        `;
      }

      rendered = rendered.replace(/{% for listing in featured_listings %}[\s\S]*?{% endfor %}/g, featuredListingsHtml);
    }

    if (options.recent_listings) {
      let recentListingsHtml = '';
      if (options.recent_listings.length > 0) {
        options.recent_listings.forEach(listing => {
          recentListingsHtml += `
            <div class="col-md-3 mb-4">
                <div class="listing-card">
                    ${listing.images && listing.images.length > 0
                      ? `<img src="${listing.images[0]}" alt="${listing.title}" class="listing-img">`
                      : `<div class="listing-img bg-light d-flex align-items-center justify-content-center">
                          <i class="fas fa-image text-secondary" style="font-size: 3rem;"></i>
                         </div>`
                    }
                    <div class="card-body">
                        <h5 class="card-title text-truncate">${listing.title}</h5>
                        <p class="listing-price">${listing.price} ${listing.currency}</p>
                        <p class="listing-location"><i class="fas fa-map-marker-alt me-1"></i> ${listing.location}</p>
                        <p class="card-text text-muted small">${new Date(listing.created_at).toLocaleDateString('ro-RO')}</p>
                        <a href="/listings/${listing.id}" class="btn btn-sm btn-outline-primary w-100">Vezi detalii</a>
                    </div>
                </div>
            </div>
          `;
        });
      } else {
        recentListingsHtml = `
          <div class="col-12 text-center py-5">
              <p class="text-muted">Nu există anunțuri momentan.</p>
          </div>
        `;
      }

      rendered = rendered.replace(/{% for listing in recent_listings %}[\s\S]*?{% endfor %}/g, recentListingsHtml);
    }

    callback(null, rendered);
  });
});

// Home route
app.get('/', async (req, res) => {
  try {
    // Get all categories
    const categoriesResult = await pool.query('SELECT * FROM categories');

    // Get featured listings
    const featuredListingsResult = await pool.query(`
      SELECT * FROM listings
      WHERE status = 'active' AND is_featured = TRUE
      ORDER BY created_at DESC
      LIMIT 8
    `);

    // Get recent listings
    const recentListingsResult = await pool.query(`
      SELECT * FROM listings
      WHERE status = 'active'
      ORDER BY created_at DESC
      LIMIT 8
    `);

    res.render(path.join(__dirname, 'marketplace/templates/marketplace/index.html'), {
      categories: categoriesResult.rows,
      featured_listings: featuredListingsResult.rows,
      recent_listings: recentListingsResult.rows
    });
  } catch (error) {
    console.error('Error rendering homepage:', error);
    res.status(500).send('Server error');
  }
});

// Listings route
app.get('/listings/:id', async (req, res) => {
  try {
    const listingId = req.params.id;
    const result = await pool.query('SELECT * FROM listings WHERE id = $1', [listingId]);

    if (result.rows.length === 0) {
      return res.status(404).send('Listing not found');
    }

    res.json(result.rows[0]);
  } catch (error) {
    console.error('Error fetching listing:', error);
    res.status(500).send('Server error');
  }
});

// API routes
app.get('/api/listings', async (req, res) => {
  try {
    let query = 'SELECT * FROM listings WHERE status = $1';
    const queryParams = ['active'];

    // Add search filter if provided
    if (req.query.search) {
      query += ' AND (title ILIKE $2 OR description ILIKE $2)';
      queryParams.push(`%${req.query.search}%`);
    }

    // Add category filter if provided
    if (req.query.category) {
      const paramIndex = queryParams.length + 1;
      query += ` AND (category_id = $${paramIndex} OR subcategory_id = $${paramIndex})`;
      queryParams.push(req.query.category);
    }

    query += ' ORDER BY created_at DESC';

    const result = await pool.query(query, queryParams);
    res.json(result.rows);
  } catch (error) {
    console.error('Error fetching listings:', error);
    res.status(500).json({ error: error.message });
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
