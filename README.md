# Cognitive Science Flanker Task Experiment

This project implements a cognitive science experiment based on the **Flanker Task**.  
Participants complete **4 modules**, each containing a **practice phase** and an **experiment phase**.  
Random **attention check** trials appear throughout the task to ensure participant engagement.

---

## 📦 Requirements

- Python 3.8+
- Pygame (installed below using pip)

---

## 🔧 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/nikhilg2603/cgs401
```

## 📦 Setup & Installation

### 1. Navigate into the Project Folder
```bash
cd cgs401
```

### 2. Create a Python Virtual Environment
```bash
python3 -m venv flanker
```

### 3. Activate the Virtual Environment
```bash
source flanker/bin/activate
```

On Windows:
```bash
flanker\Scripts\activate
```

### 4. Install Required Dependencies
```bash
pip install pygame
```

## Running the Experiment
Ensure your virtual environment is activated, then run:
```bash
python games.py
```

## Output Data
All experiment results are automatically saved to:
```
participant_id.csv
```

* Only experiment-phase trials are recorded (practice trials are not logged).
* Attention check performance is included in the results.

---
