import os
from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from supabase import create_client
from urllib.parse import quote_plus

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
SUPABASE_BUCKET = os.environ.get("SUPABASE_BUCKET", "media")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

class SupabaseStorage(Storage):
    def _save(self, name, content):
        """Uploads a file to Supabase Storage"""
        path = f"{SUPABASE_BUCKET}/{name}"
        data = content.read()

        res = supabase.storage.from_(SUPABASE_BUCKET).upload(name, data)
        if res.get("error"):
            raise Exception(f"Supabase upload failed: {res['error']['message']}")
        return name

    def url(self, name):
        """Returns the public URL for the file"""
        encoded_name = quote_plus(name)
        return f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{encoded_name}"

    def exists(self, name):
        """Checks if a file exists"""
        res = supabase.storage.from_(SUPABASE_BUCKET).list(path=name)
        return len(res) > 0
