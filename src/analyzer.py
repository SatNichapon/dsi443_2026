import time
import json
import logging
import concurrent.futures
from google import genai
from google.genai import types
from config import YOUTUBE_DATA_API_KEY , GEMINI_API_KEY
import config
import os

logger = logging.getLogger(__name__)

class RateLimitError(Exception):
    pass

def analyze_single_video(video_data: dict) -> dict | None:
    client = genai.Client(api_key=config.GEMINI_API_KEY)
    url = video_data['url']

    try:
        logger.info(f"Checking: {url}")

        response = client.models.generate_content(
            model=config.MODEL_NAME,
            config=types.GenerateContentConfig(
                system_instruction=config.PROMPT_MESSAGE,
                response_mime_type="application/json"
            ),
            contents=[
                types.Part.from_uri(file_uri=url, mime_type="video/mp4"),
                f"Analyze : '{video_data['title']}'"
            ]
        )
        ai_result = json.loads(response.text)

        final_record = {
            **video_data,
            **ai_result
        }

        logger.info(f"Success for video_id={video_data.get('video_id')}")
        return final_record

    except Exception as e:
        error_msg = str(e)

        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            logger.error(f"Rate limit hit on {url}: {e}")
            raise RateLimitError(error_msg)

        logger.error(f"Fatal Error on {url}: {e}")
        return None

def run_analysis_to_individual_files(
    video_list: list[dict],
    out_dir: str = r"D:\TU\4_y\DSI443\dsi443_2025\output\analysis_results"
) -> None:
  
    os.makedirs(out_dir, exist_ok=True)

    existing_files = set(os.listdir(out_dir))

    for idx, video in enumerate(video_list, start=1):
        vid = video.get("video_id")
        if not vid:
            logger.warning(f"Skip video with no video_id: {video}")
            continue

        index_in_query = video.get("index_in_query", "NA")
        query = video.get("query", "NA").replace(" ", "_")
        filename2 = f"{query}_{index_in_query}.json"

        # filename = f"{vid}.json"

        # out_path = os.path.join(out_dir, filename)

        if filename2 in existing_files:
            logger.info(f"[{idx}/{len(video_list)}] Skip already-processed video_id={filename2}")
            continue

        logger.info(f"[{idx}/{len(video_list)}] Analyzing video_id={filename2}")

        try:
            result = analyze_single_video(video)
        except RateLimitError:
            logger.warning(
                "Rate limit encountered. Stopping analysis. "
            )
            break  
        
        out_path2 = os.path.join(out_dir, filename2)
        if result:
            with open(out_path2, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            logger.info(f"Saved result -> {out_path2}")
        else:
            logger.info(f"No result for video_id={vid} (skipped)")

def load_all_analysis_results(out_dir: str = r"D:\TU\4_y\DSI443\dsi443_2025\output\analysis_results") -> list[dict]:

    if not os.path.exists(out_dir):
        return []

    records: list[dict] = []
    for fname in os.listdir(out_dir):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(out_dir, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                rec = json.load(f)
                records.append(rec)
        except Exception as e:
            logger.error(f"Error reading {fpath}: {e}")
            continue

    return records


def run_analysis_pipeline(video_list: list[dict]) -> list[dict]:
    results: list[dict] = []

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=config.MAX_WORKERS_ANALYSIS
    ) as executor:
        future_to_video = {
            executor.submit(analyze_single_video, video): video
            for video in video_list
        }

        try:
            for future in concurrent.futures.as_completed(future_to_video):
                try:
                    data = future.result()
                except RateLimitError:
                    logger.warning(
                        "Rate limit"
                    )
                    for f in future_to_video:
                        if not f.done():
                            f.cancel()
                    break 

                except Exception as e:
                    logger.error(f"Unexpected error in analysis: {e}")
                    continue

                if data:
                    results.append(data)

                time.sleep(config.DELAY_SECONDS)

        finally:
            return results
