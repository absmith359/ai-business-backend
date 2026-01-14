from pydantic import BaseModel

class Business(BaseModel):
    id: str
    name: str
    owner_name: str
    email: str
    phone: str | None = None

    # AI settings
    custom_prompt: str | None = None
    greeting: str | None = None

    # Branding
    primary_color: str | None = None
    secondary_color: str | None = None
    logo_url: str | None = None

    # Widget settings
    widget_position: str | None = None
    welcome_message: str | None = None
    show_typing_indicator: bool | None = None
    enable_lead_capture: bool | None = None