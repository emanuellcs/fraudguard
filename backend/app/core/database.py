import asyncpg
from app.core.config import settings

class DatabasePool:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(dsn=settings.DATABASE_URL)

    async def disconnect(self):
        if self.pool:
            await self.pool.close()

    async def log_transaction(self, amount, time, pca, risk_score, is_fraud):
        """
        Executes raw SQL to log the transaction and prediction.
        """
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                # Insert into transactions_log
                # We cast the pca dict to jsonb
                row = await conn.fetchrow("""
                    INSERT INTO transactions_log (amount, seconds_elapsed, pca_vector)
                    VALUES ($1, $2, $3::jsonb)
                    RETURNING id;
                """, amount, time, pca)
                
                txn_id = row['id']

                # Insert into fraud_predictions
                await conn.execute("""
                    INSERT INTO fraud_predictions (transaction_id, risk_score, prediction_class)
                    VALUES ($1, $2, $3);
                """, txn_id, risk_score, int(is_fraud))
                
                return str(txn_id)

db = DatabasePool()