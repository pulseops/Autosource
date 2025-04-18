from faker import Faker
from typing import Optional
import random
import string

_FAKER_INSTANCE: Optional[Faker] = None

def get_faker() -> Faker:
    """Get or create a singleton Faker instance."""
    global _FAKER_INSTANCE
    if _FAKER_INSTANCE is None:
        _FAKER_INSTANCE = Faker()
    return _FAKER_INSTANCE

def generate_id(prefix: str = "", length: int = 8) -> str:
    """Generate a random ID with an optional prefix."""
    chars = string.ascii_lowercase + string.digits
    random_part = ''.join(random.choices(chars, k=length))
    return f"{prefix}_{random_part}" if prefix else random_part

def generate_timestamp(base_date, offset_days: int = 0, offset_hours: int = 0) -> str:
    """Generate an ISO 8601 timestamp with the given offsets."""
    date = base_date
    if offset_days:
        date = date.replace(day=date.day + offset_days)
    if offset_hours:
        date = date.replace(hour=date.hour + offset_hours)
    return date.isoformat()

def generate_company_name() -> str:
    """Generate a realistic company name."""
    faker = get_faker()
    patterns = [
        lambda: f"{faker.word().capitalize()}Stack",
        lambda: f"{faker.word().capitalize()}Labs",
        lambda: f"{faker.word().capitalize()}AI",
        lambda: f"{faker.word().capitalize()}{faker.word().capitalize()}",
    ]
    return random.choice(patterns)()

def generate_user_name() -> str:
    """Generate a realistic username."""
    faker = get_faker()
    return faker.user_name()

def generate_email(name: Optional[str] = None) -> str:
    """Generate a realistic email address."""
    faker = get_faker()
    if name is None:
        name = generate_user_name()
    domain = random.choice(["gmail.com", "yahoo.com", "hotmail.com", "company.com"])
    return f"{name}@{domain}"

def generate_url() -> str:
    """Generate a realistic URL."""
    faker = get_faker()
    return faker.url()

def generate_version() -> str:
    """Generate a semantic version number."""
    major = random.randint(0, 3)
    minor = random.randint(0, 9)
    patch = random.randint(0, 99)
    return f"{major}.{minor}.{patch}"

def generate_error_message() -> str:
    """Generate a realistic error message."""
    templates = [
        "Connection refused",
        "Invalid authentication credentials",
        "Resource not found",
        "Permission denied",
        "Rate limit exceeded",
        "Internal server error",
        "Service unavailable",
        "Invalid request format",
    ]
    return random.choice(templates)
