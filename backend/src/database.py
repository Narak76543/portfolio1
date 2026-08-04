"""Supabase client factory.

Creates a single Supabase client instance using the service-role key
(backend-only — never exposed to frontend).
"""

from supabase import Client, create_client

from src.config import settings

_client: Client | None = None


def get_supabase_client() -> Client:
    """Return a singleton Supabase client."""
    global _client
    if _client is None:
        _client = create_client(
            settings.supabase_url,
            settings.supabase_service_role_key,
        )
    return _client
