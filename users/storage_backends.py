import os
from io import BytesIO
from urllib.parse import quote
from django.core.files.base import File
from django.core.files.storage import Storage
from supabase import create_client, Client

# Environment variables
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
SUPABASE_BUCKET = os.environ.get("SUPABASE_BUCKET", "media")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class SupabaseStorage(Storage):
    """
    Custom Django storage backend using Supabase Storage.
    """

    def _open(self, name, mode='rb'):
        """Download a file from Supabase and return as Django File object"""
        res = supabase.storage.from_(SUPABASE_BUCKET).download(name)
        if res is None:
            raise FileNotFoundError(f"{name} not found in Supabase bucket")
        return File(BytesIO(res), name=name)

    def _save(self, name, content):
    """Upload a file to Supabase"""
    data = content.read()
    if isinstance(data, str):
        data = data.encode('utf-8')  # ensure bytes

    # Remove `upsert=True`, just upload bytes
    res = supabase.storage.from_(SUPABASE_BUCKET).upload(name, data)
    
    # Check for errors
    if res.get("error"):
        raise Exception(f"Supabase upload failed: {res['error']['message']}")
    return name


    def exists(self, name):
        """Check if a file exists in Supabase"""
        files = supabase.storage.from_(SUPABASE_BUCKET).list()
        return any(f['name'] == name for f in files)

    def delete(self, name):
        """Delete a file from Supabase"""
        res = supabase.storage.from_(SUPABASE_BUCKET).remove([name])
        if res.get("error"):
            raise Exception(f"Supabase delete failed: {res['error']['message']}")

    def url(self, name):
        """Return public URL for the file"""
        return f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{quote(name, safe='/')}"

    def size(self, name):
        """Get size of the file in bytes"""
        res = supabase.storage.from_(SUPABASE_BUCKET).download(name)
        if res is None:
            return 0
        return len(res)

    def listdir(self, path):
        """List files and directories in a bucket path"""
        files = supabase.storage.from_(SUPABASE_BUCKET).list(path=path)
        directories, filenames = [], []
        for f in files:
            if f['type'] == 'folder':
                directories.append(f['name'])
            else:
                filenames.append(f['name'])
        return directories, filenames
