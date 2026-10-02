"""EduGenie command-processing module."""
from datetime import datetime
from pathlib import Path
import re
import os
import wikipedia
import pyjokes

BASE_DIR = Path(__file__).resolve().parent
NAME_FILE = Path(os.environ.get("EDUGENIE_NAME_FILE", str(BASE_DIR / "assistant_name.txt")))

def load_name():
    try:
        name = NAME_FILE.read_text(encoding="utf-8").strip()
        return name[:40] if name else "EduGenie"
    except (FileNotFoundError, OSError):
        return "EduGenie"

def _reply(message, status="success", **extra):
    return {"status": status, "response": message, **extra}

def process_command(query):
    if not isinstance(query, str) or not query.strip():
        return _reply("Please enter a command.", "error")
    original = query.strip()
    q = re.sub(r"\\s+", " ", original.lower())

    if q in {"hi", "hello", "hey", "good morning", "good afternoon", "good evening"}:
        return _reply(f"Hello! I am {load_name()}. How can I help you today?")
    if q in {"time", "what is the time", "what time is it", "current time"} or "current time" in q:
        return _reply("The current time is " + datetime.now().strftime("%I:%M:%S %p") + ".")
    if q in {"date", "today", "today's date", "what is the date"} or "today's date" in q:
        return _reply("Today's date is " + datetime.now().strftime("%d %B %Y") + ".")
    if "wikipedia" in q or q.startswith("search "):
        term = re.sub(r"^(search wikipedia for|search|wikipedia)\\s*", "", original, flags=re.I).strip()
        if not term:
            return _reply("Please tell me what you want to search on Wikipedia.")
        try:
            return _reply(wikipedia.summary(term, sentences=3, auto_suggest=True))
        except wikipedia.exceptions.DisambiguationError:
            return _reply("I found several matching topics. Please make your search more specific.")
        except wikipedia.exceptions.PageError:
            return _reply("I couldn't find a matching Wikipedia page.")
        except Exception:
            return _reply("Wikipedia is unavailable right now. Please try again.")
    if "joke" in q:
        try:
            return _reply(pyjokes.get_joke())
        except Exception:
            return _reply("I couldn't get a joke right now.", "error")
    if "open youtube" in q:
        return _reply("Opening YouTube in a new tab.", url="https://www.youtube.com", action="redirect")
    if "open google" in q:
        return _reply("Opening Google in a new tab.", url="https://www.google.com", action="redirect")
    prefix = "change your name to"
    if q.startswith(prefix):
        new_name = original[len(prefix):].strip()
        if not new_name or len(new_name) > 40 or any(ord(c) < 32 for c in new_name):
            return _reply("Please provide a name containing 1 to 40 characters.", "error")
        try:
            NAME_FILE.write_text(new_name, encoding="utf-8")
            return _reply(f"Okay! You can call me {new_name} from now on.", assistant_name=new_name)
        except OSError:
            return _reply("I couldn't save the new name. This host may use temporary storage.", "error")
    return _reply(
        f"I received: “{original}”. Try: time, date, joke, Wikipedia [topic], "
        "open Google, open YouTube, or change your name to [name]."
    )
