# pgVector Database Setup

## Configuration Details

- **Container Name**: pgvector
- **Image**: pgvector/pgvector:pg16
- **Port**: 5433 (mapped to 5432 inside container)
- **Database Name**: vectordb
- **Username**: postgres
- **Password**: postgres

## Connection String
```
postgresql://postgres:postgres@localhost:5433/vectordb
```

## Environment Variables (.env.local)
```
PGVECTOR_HOST=localhost
PGVECTOR_PORT=5433
PGVECTOR_DB=vectordb
PGVECTOR_USER=postgres
PGVECTOR_PASSWORD=postgres
```

## Using pgVector for Chunks and Condensed Content

1. First connect to the database:
```bash
psql -h localhost -p 5433 -U postgres -d vectordb
```

2. Enable the vector extension:
```sql
CREATE EXTENSION vector;
```

3. Create a table for chunks:
```sql
CREATE TABLE document_chunks (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding vector(1536),
    metadata JSONB
);
```

4. Create a table for condensed content:
```sql
CREATE TABLE condensed_content (
    id SERIAL PRIMARY KEY,
    summary TEXT,
    embedding vector(1536),
    source_ids INTEGER[]
);
```

## Basic Vector Operations

```sql
-- Insert a vector
INSERT INTO document_chunks (content, embedding) 
VALUES ('sample text', '[1.0, 2.0, 3.0]');

-- Find similar vectors
SELECT id, content 
FROM document_chunks 
ORDER BY embedding <-> '[1.0, 2.0, 3.0]' 
LIMIT 5;
```

## Maintenance
- To stop container: `docker stop pgvector`
- To start container: `docker start pgvector`
- To remove container: `docker rm pgvector`