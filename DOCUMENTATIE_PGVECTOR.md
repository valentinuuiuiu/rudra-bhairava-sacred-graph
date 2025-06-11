# Documentație Configurare pgvector

## 1. Configurarea containerului Docker

Pentru a rula pgvector într-un container Docker pe portul 5433, folosiți următoarea comandă:

```bash
docker run --name pgvector-container \
  -e POSTGRES_USER=nume_utilizator \
  -e POSTGRES_PASSWORD=parola_secreta \
  -e POSTGRES_DB=nume_baza_date \
  -p 5433:5432 \
  -d ankane/pgvector:latest
```

Explicații parametri:
- `--name`: Numele containerului
- `-e`: Variabile de mediu pentru configurare
- `-p`: Mapare porturi (5433 extern la 5432 intern)
- `-d`: Rulează în modul detached

## 2. Credențiale de conectare

Structura credențialelor (înlocuiți cu valorile reale):

```env
DB_HOST=localhost
DB_PORT=5433
DB_NAME=nume_baza_date
DB_USER=nume_utilizator
DB_PASSWORD=parola_secreta
```

## 3. Crearea tabelelor

### Tabel pentru chunks

```sql
CREATE TABLE document_chunks (
  id SERIAL PRIMARY KEY,
  document_id INTEGER NOT NULL,
  chunk_text TEXT NOT NULL,
  embedding VECTOR(1536),  -- Dimensiunea vectorului
  created_at TIMESTAMP DEFAULT NOW()
);
```

### Tabel pentru condensed content

```sql
CREATE TABLE condensed_content (
  id SERIAL PRIMARY KEY,
  document_id INTEGER NOT NULL,
  summary TEXT NOT NULL,
  embedding VECTOR(1536),
  created_at TIMESTAMP DEFAULT NOW()
);
```

## 4. Operații de bază cu vectori

### Inserare vector

```sql
INSERT INTO document_chunks (document_id, chunk_text, embedding)
VALUES (1, 'Text exemplu', '[0.1, 0.2, ..., 0.5]');
```

### Căutare similaritate

```sql
SELECT id, chunk_text, 1 - (embedding <=> '[0.1, 0.3, ..., 0.4]') AS similarity
FROM document_chunks
ORDER BY embedding <=> '[0.1, 0.3, ..., 0.4]'
LIMIT 5;
```

### Actualizare vector

```sql
UPDATE document_chunks
SET embedding = '[0.5, 0.1, ..., 0.9]'
WHERE id = 1;
```

## 5. Gestionarea containerului

### Pornire container

```bash
docker start pgvector-container
```

### Oprire container

```bash
docker stop pgvector-container
```

### Restart container

```bash
docker restart pgvector-container
```

### Vizualizare logs

```bash
docker logs pgvector-container
```

### Ștergere container

```bash
docker rm pgvector-container
```

## Observații importante

1. Asigurați-vă că aveți Docker instalat
2. Portul 5433 nu trebuie să fie ocupat de alt serviciu
3. Pentru performanță optimă, alocați suficiente resurse containerului
4. Păstrați credențiale în fișiere securizate (.env)
5. Dimensiunea vectorilor trebuie să corespundă cu modelul folosit