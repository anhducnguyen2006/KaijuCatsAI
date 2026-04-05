# Kaiju Cats AI - Game Simulation

A Python simulation prototype for a Roblox-inspired game concept where giant cats navigate a 5x5 map containing buildings, power plants, and obstacles.

## Features

- Procedural 5x5 map generation with constrained/random tile placement
- Distinct tile types with gameplay effects:
  - `HV` (High Value Building)
  - `LV` (Low Value Building)
  - `PP` (Power Plant)
  - `M` (Mud)
  - `ST` (Spike Trap)
  - `B` (Boulder)
  - `ET` (Empty Tile)
- Command system design with costs (`N`, `S`, `E`, `W`, `SP`, `PU`)
- Multi-cat starting and target bed positions prepared for simulation logic

## Project Structure

- `GameSimulation.py`: main simulation script
- `requirements.txt`: Python dependencies

## Getting Started

### 1. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the simulation

```bash
python GameSimulation.py
```

You should see the generated game map printed in the terminal.

## Notes

- This repository currently focuses on map generation and core rule scaffolding.
- Additional gameplay loop and cat action execution logic can be built on top of the existing structure.

## License

This project is licensed under the MIT License. See `LICENCE` for details.
