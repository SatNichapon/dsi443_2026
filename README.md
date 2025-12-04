# DSI443 Project: Charlie Kirk's News Narrative Analysis Pipeline

A data pipeline that collects YouTube video metadata and uses Google Gemini AI to extract narrative structures, sentiment, and conflict dynamics for political discourse analysis.

## Overview

This project automates the collection and analysis of YouTube videos through a two-phase pipeline:

1. **Collection Phase**: Searches YouTube for videos matching predefined queries and collects metadata (title, date, URL, description)
2. **Analysis Phase**: Uses Google Gemini 2.0 Flash AI to analyze video content and extract structured insights in JSON format

## Architecture

```
            SEARCH QUERIES  
                    |
                    v
    [Collector] search_youtube_query()  
                    |
                    v
      Unique video metadata list 
                    |
                    v
    [Analyzer] analyze_single_video()    
                    |
                    v
    Gemini 2.0 Flash --> JSON output
                    |
                    v
                  Merge 
                    |
                    v
             analyze_timeline.json
```

## Project Structure

```
.
 main.py                 # Entry point for the pipeline
 pyproject.toml         # Project dependencies
 README.md              # This file
 src/
    __init__.py
    collector.py       # YouTube data collection module
    analyzer.py        # Gemini AI analysis module
    config.py          # Configuration and API keys
    prompts.yaml       # AI prompt templates
 output/
     target_videos.json         # Collected video metadata (checkpoint)
     final_analysis_results.json # Merged analysis results
     pipeline.log               # Execution log
     analysis_results/          # Individual analysis results
         ├── Charlie_Kirk_Fox_Business_2011_0.json
         ├── Charlie_Kirk_Fox_Business_2011_1.json
         └── ...
```

## Requirements

- Python 3.11+
- Google YouTube Data API key
- Google Gemini API key
- Internet connection (for API access)

## Installation

1. **Clone or download this repository**

2. **Install dependencies** using pip or your Python package manager:
   ```bash
   pip install google-api-python-client google-genai python-dotenv pyyaml
   ```

   Or with uv:
   ```bash
   uv sync
   ```

3. **Set up API keys** by creating a `.env` file in the project root:
   ```
   YOUTUBE_DATA_API_KEY=your_youtube_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

   **How to obtain API keys:**
   - **YouTube API**: Go to [Google Cloud Console](https://console.cloud.google.com/), create a project, enable YouTube Data API v3, and generate an API key
   - **Gemini API**: Go to [Google AI Studio](https://aistudio.google.com/app/apikey) and create an API key

4. **Configure search queries** (optional):
   - Edit `src/config.py` and modify the `SEARCH_QUERIES` list to search for different topics
   - Customize the AI prompt in `src/prompts.yaml` to analyze videos differently

## Usage

Run the pipeline:

```bash
python main.py
```
Or with uv:
```bash
uv run main.py
```

The pipeline will:
1. **Check for cached data**: If videos were already collected, you'll be asked whether to reuse them
2. **Collect videos**: If no cache exists, the Collector searches YouTube for all queries and saves results to `output/target_videos.json`
3. **Analyze videos**: The Analyzer processes each video with Gemini AI and saves individual JSON results to `output/analysis_results/`
4. **Finalize**: Loads all individual analysis results and merges them into `output/final_analysis_results.json`

All activity is logged to `output/pipeline.log`.

## Configuration

### Key Settings in `src/config.py`:

- **`SEARCH_QUERIES`**: List of YouTube search terms (currently only "Charlie Kirk Fox Business 2011" is active; others are commented out)
- **`MAX_VIDEOS_PER_QUERY`**: Maximum videos to collect per search query (default: 5)
- **`MODEL_NAME`**: AI model to use for analysis (default: "gemini-2.0-flash-lite")
- **`DELAY_SECONDS`**: Delay between API calls to respect rate limits (default: 50 seconds)

### Customizing Analysis

Edit `src/prompts.yaml` to change the AI analysis prompt. The current prompt analyzes narrative structures, sentiment, and conflict dynamics. Modify the `charlie_v4` section to adjust what insights are extracted.

## Output Format

The analysis generates two types of outputs:

1. **Individual Results** in `output/analysis_results/`:
   - Named as `{query}_{index}.json` (e.g., `Charlie_Kirk_Fox_Business_2011_0.json`)
   - Each file contains the merged video metadata + AI analysis for one video
   - Skips re-processing if a file already exists

2. **Merged Summary** in `output/final_analysis_results.json`:
   - Loads all individual JSON files from `analysis_results/` and combines them
   - Single file containing array of all analyzed videos

Example record structure:
```json
{
  "query": "Charlie Kirk Fox Business 2011",
  "video_id": "YouTube video ID",
  "url": "https://www.youtube.com/watch?v=...",
  "title": "Video title",
  "publish_date": "ISO 8601 date",
  "description": "Video description",
  "index_in_query": 0,
  "[AI analysis fields]": "..."
}
```

The exact structure of AI analysis fields depends on your prompt configuration in `src/prompts.yaml`.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `WARNING: YOUTUBE_DATA_API_KEY is missing` | Ensure `.env` file exists in project root with correct API keys |
| `WARNING: GEMINI_API_KEY is missing` | Check that both API keys are set in `.env` |
| Rate limit errors (HTTP 429) | The pipeline respects rate limits. Try increase `DELAY_SECONDS` |
| No videos found | Verify your search queries are valid YouTube search terms |
| Analysis returns empty results | Check your prompt configuration in `src/prompts.yaml` |

## Dependencies

- **google-api-python-client**: YouTube API client
- **google-genai**: Google Gemini AI API client
- **python-dotenv**: Environment variable management
- **pyyaml**: YAML prompt configuration parsing

## Notes

- The pipeline caches collected videos in `output/target_videos.json` to avoid redundant API calls
- Individual analysis results are saved to `output/analysis_results/` with names like `{query}_{index}.json`
- Already-processed videos are skipped automatically (based on filename matching)
- Analysis respects Gemini API rate limits with configurable delays
- All operations are logged to `output/pipeline.log` for debugging
- Videos are deduplicated based on video ID during collection

## License

No License

## Contact

LinkedIn: https://www.linkedin.com/in/satnichapon/
