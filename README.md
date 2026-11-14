# Andromia Health Co-pilot

NASA Space Apps Challenge Hackathon Submission

Andromia health co-pilot is a small project i made for 2026 NASA Space Apps Challenge.

The purpose of this tool is to log the astronaut health data, which visualise the given data into a beautiful graph and provide aditional information about the user.

## Features

- Split-scale graph: Utilizes chart.js to map high variance metrics
- Offline architecture: Runs on local sqlite database, no external apis
- Locked view interface: Single page application that locks the view port
- Psycological tracking: Uses UCLA Lonliness scale to asses mental health

## Tech Stack

- Backend: Python3, Flask
- Database: Sqlite3
- Frontend: html, css, js

## Installation

1. Clone the repository

```bash
git clone https://github.com/pranav10780/andromia.git
cd andromia
```

2. Create and Activate a Virtual Environment

```bash
python3 -m venv .venv
. .venv/bin/activate
```

3. Install Dependencies

```bash
pip install Flask
```

4. Run
```bash
python3 app.py
```

>NOTE: It will generate the `localhealth.db` on its first run.

5. Browser
```
Open your browser and navigate to http://localhost:8080
```

## Limitaitons

- Manual data entry - No automated telemetry entry option
- Static rules engine - Hardcoded if/else diagnostics
- Single user focused - Made for one user only

## License

This project is under MIT License
