## Setup Instructions
1. Start the PostgreSQL database container:
   ```bash
   docker compose up -d
   ```

2. Connect to the database:
   - Without GUI:
     ```bash
     docker compose exec db psql -U interview_user -d interview_db
     ```
   - With GUI: Use DBeaver or any PostgreSQL-compatible client

3. Initialize sample data:
   ```sql
   \i /docker-entrypoint-initdb.d/init.sql
   ```