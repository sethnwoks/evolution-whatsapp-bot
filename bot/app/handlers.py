"""
Message handlers and command routing logic.
This keeps main.py clean and makes it easy to add new commands.
"""

def route_message(text: str) -> str:
    """
    Route incoming messages to appropriate handlers.
    
    Args:
        text: The incoming message text (already lowercased and stripped)
    
    Returns:
        Reply text to send back
    """
    # Greeting commands
    if any(word in text for word in ["hi", "hello", "fire"]):
        return handle_greeting()
    
    # Demo command
    elif "demo" in text:
        return handle_demo()
    
    # Help command
    elif text in ["help", "commands", "?"]:
        return handle_help()
    
    # Status check
    elif text == "status":
        return handle_status()
    
    # Default fallback
    else:
        return handle_unknown()


def handle_greeting() -> str:
    """Handle greeting messages"""
    return "🔥 *FASTAPI MODE ACTIVATED!* 🚀\n\nThe brain has been upgraded to a high-performance engine."


def handle_demo() -> str:
    """Handle demo command"""
    return "🤖 Running on FastAPI + Uvicorn."


def handle_help() -> str:
    """Show available commands"""
    return """
📋 *Available Commands:*

• hi/hello - Greeting
• demo - See tech stack
• status - Check bot status
• help - Show this message

🚀 More features coming soon!
"""


def handle_status() -> str:
    """Check bot status"""
    return "✅ Bot is online and operational!"


def handle_unknown() -> str:
    """Handle unknown commands"""
    return "🤔 I didn't understand that. Type *help* to see available commands."
