"""Global application settings loaded from environment variables.

Uses pydantic-settings so env vars are never hardcoded anywhere in the
codebase (including Supabase URL/keys).
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings — populated from .env / environment."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Supabase
    supabase_url: str
    supabase_service_role_key: str
    supabase_anon_key: str

    # CORS
    cors_origins: str = "http://localhost:3000,http://localhost:3001,http://localhost:3002"

    @property
    def cors_origin_list(self) -> list[str]:
        """Parse comma-separated CORS origins into a list."""
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()  # type: ignore[call-arg]
