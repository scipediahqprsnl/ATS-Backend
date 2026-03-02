# ATS Resume Ranking Prototype

## Overview
Dynamic resume ranking system that evaluates candidates against job descriptions using skill matching and experience-aware scoring.

## Features
- PDF resume parsing
- Automatic experience extraction
- Dynamic JD parsing
- Skill-based scoring (65%)
- Experience-aware scoring (35%)
- Overqualification penalty
- Talent pool persistence with multi-role tracking
- JD-based reranking

## Architecture
- parser/
- scoring/
- services/
- jd/
- main.py

## Status Logic
- SHORTLIST
- REVIEW
- TALENT_POOL

## Next Improvements
- Skill weighting
- Domain filtering
- Semantic similarity
- Async ingestion

## Entry Point
Main execution file:  main.py

To run:
- python main.py
