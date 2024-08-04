from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
private_key: str = os.getenv("SUPABASE_SECRET_KEY")


supabaseClient: Client = create_client(url, private_key)
