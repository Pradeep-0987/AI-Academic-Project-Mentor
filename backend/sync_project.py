import uuid
from sqlalchemy import text
from app.database.session import engine

def sync():
    with engine.connect() as conn:
        user = conn.execute(text("SELECT id FROM users WHERE email = 'priyanka@test.com'")).fetchone()
        if not user:
            print("User priyanka@test.com not found")
            return
        
        user_id = user[0]
        # Check if project exists
        existing = conn.execute(
            text("SELECT id, title FROM projects WHERE student_id = :sid"),
            {"sid": user_id}
        ).fetchall()
        
        if not existing:
            new_id = uuid.uuid4()
            conn.execute(
                text("""
                    INSERT INTO projects (id, student_id, title, description, status)
                    VALUES (:id, :sid, :title, :description, :status)
                """),
                {
                    "id": new_id,
                    "sid": user_id,
                    "title": "AI-Based Financial Analysis",
                    "description": "Predictive financial modeling, market sentiment analysis, and risk assessment using deep learning.",
                    "status": "In Progress"
                }
            )
            conn.commit()
            print(f"Successfully inserted project 'AI-Based Financial Analysis' (ID: {new_id}) into Supabase for user {user_id}!")
        else:
            print(f"Projects already in Supabase for user: {existing}")

if __name__ == "__main__":
    sync()
