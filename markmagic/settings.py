"""Settings for markdown conversion."""

from typing import Literal

from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from tabulate import tabulate_formats


class Settings(BaseSettings):
    """Markdown conversion settings."""

    # Email settings
    process_attachments: bool = True
    # Excel settings
    skip_empty_area: bool = False
    # PDF settings
    extraction_mode: Literal["plain", "layout"] = "plain"
    use_vlm: bool = False
    model: str = "meta-llama/Llama-Vision-Free"
    # model: str = "Qwen/Qwen2-VL-72B-Instruct"
    api_key: SecretStr | None = None
    base_url: str = "https://api.together.xyz/v1"
    stop: list[str] | None = ["<|eot_id|>", "<|eom_id|>"]
    # stop: list[str] | None = ["<|im_end|>", "<|endoftext|>"]
    # Table settings
    tablefmt: str = "github"  # Type checkers do not support unpacking into a Literal
    showindex: bool = False
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @field_validator("tablefmt")
    def validate_tablefmt(cls, v: str) -> str:
        """Validate tablefmt."""
        assert v in tabulate_formats
        return v
