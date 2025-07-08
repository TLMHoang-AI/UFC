# UFC Fight Analysis & Local Streamlit Dashboard

This project provides an interactive dashboard for exploring UFC fighter statistics, comparing fighter performance, and analyzing match outcomes. Built using **Pandas**, **Plotly**, and **Streamlit**, the application enables users to gain insights into fighters' historical data, strengths, and trends across weight classes and events.

## Overview

The application supports three main analysis sections:

1. **Fighter Overview** – View detailed stats, win methods, and performance metrics for a selected fighter.
2. **Compare Fighters** – Compare two fighters head-to-head across key metrics and fighting locations.
3. **Matches Highlights** – Explore individual matches, including outcome, round/time, and fighter stat comparison.

All sections are integrated into a responsive local Streamlit dashboard with interactive visualizations.

## Features

### 1. Fighter Overview
- View basic details: name, nickname, total fights, wins, losses, draws.
- Visualize distribution of fights across weight classes.
- Display win methods (KO/TKO, submission, decision) as a bar chart.
- View a radar chart of performance metrics:
  - Striking Accuracy
  - Takedown Accuracy
  - Strike Defense
  - Takedown Defense
  - Knockdown Avg
  - Submission Avg

### 2. Compare Fighters
- Select any two fighters from the dataset.
- Display their top fighting locations and win rates there.
- Show side-by-side stat comparison.
- Render a dual radar chart for performance metrics.

### 3. Matches Highlights
- Select any recorded match from historical data.
- View match details: weight class, round/time, total rounds.
- Compare both fighters' metrics in that specific match.

## Dataset Files

Make sure the following CSV files are available locally:

- `fight_results_with_locale.csv`
- `fight_stats_with_weghtclass_date_location.csv`
- `fighters_processed.csv`

## How to Run Locally

1. Clone the repository:

```bash
git clone https://github.com/your-username/ufc-fight-analysis
cd ufc-fight-analysis
