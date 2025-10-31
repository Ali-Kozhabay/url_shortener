from celery import shared_task
from .models import Click
from shortener.models import URL


@shared_task
def track_click(url_id, ip_address, user_agent, referer):
    """Asynchronously track URL click"""
    try:
        url = URL.objects.get(id=url_id)
        
        # Parse user agent to extract device info (simplified)
        device_type = parse_device_type(user_agent)
        browser = parse_browser(user_agent)
        os = parse_os(user_agent)
        
        Click.objects.create(
            url=url,
            ip_address=ip_address,
            user_agent=user_agent,
            referer=referer if referer else None,
            device_type=device_type,
            browser=browser,
            os=os
        )
        
        return f"Tracked click for {url.short_code}"
    except URL.DoesNotExist:
        return f"URL with id {url_id} not found"


def parse_device_type(user_agent):
    """Simple device type detection"""
    user_agent_lower = user_agent.lower()
    if 'mobile' in user_agent_lower or 'android' in user_agent_lower:
        return 'mobile'
    elif 'tablet' in user_agent_lower or 'ipad' in user_agent_lower:
        return 'tablet'
    return 'desktop'


def parse_browser(user_agent):
    """Simple browser detection"""
    user_agent_lower = user_agent.lower()
    if 'chrome' in user_agent_lower:
        return 'Chrome'
    elif 'firefox' in user_agent_lower:
        return 'Firefox'
    elif 'safari' in user_agent_lower:
        return 'Safari'
    elif 'edge' in user_agent_lower:
        return 'Edge'
    return 'Unknown'


def parse_os(user_agent):
    """Simple OS detection"""
    user_agent_lower = user_agent.lower()
    if 'windows' in user_agent_lower:
        return 'Windows'
    elif 'mac' in user_agent_lower or 'ios' in user_agent_lower:
        return 'Mac/iOS'
    elif 'android' in user_agent_lower:
        return 'Android'
    elif 'linux' in user_agent_lower:
        return 'Linux'
    return 'Unknown'
