"""
Database setup script to create tables in Supabase
"""
import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_database():
    """Create the required tables in Supabase database."""
    
    # Get database URL from environment
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL not found in environment variables")
        return False
    
    try:
        # Connect to database
        print("🔌 Connecting to Supabase database...")
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Read and execute schema
        print("📝 Creating database tables...")
        
        # Users table
        users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            is_verified BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """
        
        # Password reset tokens table
        password_resets_table = """
        CREATE TABLE IF NOT EXISTS password_resets (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            email VARCHAR(255) NOT NULL,
            token VARCHAR(255) NOT NULL UNIQUE,
            expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
            used BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """
        
        # Create indexes
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);",
            "CREATE INDEX IF NOT EXISTS idx_password_resets_token ON password_resets(token);",
            "CREATE INDEX IF NOT EXISTS idx_password_resets_email ON password_resets(email);"
        ]
        
        # Create update function
        update_function = """
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
        """
        
        # Create trigger
        trigger = """
        DROP TRIGGER IF EXISTS update_users_updated_at ON users;
        CREATE TRIGGER update_users_updated_at 
            BEFORE UPDATE ON users 
            FOR EACH ROW 
            EXECUTE FUNCTION update_updated_at_column();
        """
        
        # Execute all SQL commands
        cursor.execute(users_table)
        print("✅ Users table created/verified")
        
        cursor.execute(password_resets_table)
        print("✅ Password resets table created/verified")
        
        for index in indexes:
            cursor.execute(index)
        print("✅ Indexes created/verified")
        
        cursor.execute(update_function)
        print("✅ Update function created/verified")
        
        cursor.execute(trigger)
        print("✅ Update trigger created/verified")
        
        # Commit changes
        conn.commit()
        print("🎉 Database setup completed successfully!")
        
        # Test connection by checking tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name IN ('users', 'password_resets');
        """)
        
        tables = cursor.fetchall()
        print(f"📋 Verified tables: {[table[0] for table in tables]}")
        
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
        print("🔌 Database connection closed")

if __name__ == "__main__":
    print("Setting up Supabase database...")
    print("=" * 50)
    
    success = setup_database()
    
    if success:
        print("\n✅ Database setup complete! You can now run the API server.")
    else:
        print("\n❌ Database setup failed. Please check your configuration.")
