import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# --- API KEYS ---
YOUTUBE_DATA_API_KEY = os.getenv("YOUTUBE_DATA_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not YOUTUBE_DATA_API_KEY:
    print("WARNING: YOUTUBE_DATA_API_KEY is missing from .env")
if not GEMINI_API_KEY:
    print("WARNING: GEMINI_API_KEY is missing from .env")

# --- PROJECT PATHS ---
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"
SRC_DIR = BASE_DIR / "src"

OUTPUT_DIR.mkdir(exist_ok=True)

PROMPTS_FILE = SRC_DIR / "prompts.yaml"
URL_LIST_FILE = OUTPUT_DIR / "target_videos.json"
FINAL_OUTPUT_DIR = OUTPUT_DIR / "analysis_results"
FINAL_OUTPUT_FILE = OUTPUT_DIR / "final_analysis_results.json"

FINAL_OUTPUT_DIR.mkdir(exist_ok=True)

# --- AI MODEL SETTINGS ---
MODEL_NAME = "gemini-2.0-flash-lite" 

# --- SEARCH SETTINGS ---
SEARCH_QUERIES = [
    "Charlie Kirk Fox Business 2011",
    "Charlie Kirk Turning Point USA TPUSA 2012",
    "Charlie Kirk RNC speech 2016",
    "Charlie Kirk Kent State diaper protest 2017",
    "Charlie Kirk Prove Me Wrong white privilege 2018",
    "Charlie Kirk Politicon debate Cenk Hasan 2018",
    "Charlie Kirk Show launch 2019",
    "Charlie Kirk Socialism Sucks tour 2019",
    "Charlie Kirk Groypers Q&A confrontation 2019",
    "Charlie Kirk China Lied tour lockdown 2020",
    "Charlie Kirk Critical Race Theory CRT tour 2021",
    "Charlie Kirk Educate Dont Mandate tour 2022",
    "Charlie Kirk Screaming Student Penn State 2022",
    "Charlie Kirk Only Two Genders table flip 2023",
    "Charlie Kirk UC Davis protest riot 2023",
    "Charlie Kirk abortion is murder debate 2023",
    "Charlie Kirk Party of Baal theology 2023",
    "Charlie Kirk Seven Mountain Mandate 2024",
    "Charlie Kirk Jubilee Surrounded 2024",
    "Charlie Kirk Brainwashed Haitian migrants 2024",
    "Charlie Kirk Bitcoin Reserve 2025",
    "Charlie Kirk Utah Valley University debate 2025",
    "Charlie Kirk Presidential Medal of Freedom 2025"
]

# --- ANALYSIS SETTINGS ---
MAX_VIDEOS_PER_QUERY = 5
DELAY_SECONDS = 50


# --- PROMPTS ---
def load_prompt(prompt_name="charlie_v1"):
    """
    Loads a specific prompt text from the external YAML configuration file.

    Allows for cleaner code and easier editing of large text blocks without
    modifying the Python source directly.

    Args:
        prompt_name (str): The key to look for in prompts.yaml (default: "charlie_v1").
    Returns:
        str: The content of the prompt. Returns an empty string if the file is missing
            or the key is not found.
    """
    try:
        with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return data.get(prompt_name, "")
    except FileNotFoundError:
        print("{PROMPTS_FILE}")
        return ""

# Load the prompt so other modules can import it. You can define your prompt in src/propmts.yaml
PROMPT_MESSAGE = load_prompt("charlie_v4") # << change to your prompts