# 🐾 Pet Name Oracle 🔮

A mystical CLI tool that generates hilarious or mystical pet names based on pet type, personality, and user quirks. Each name comes with its own magical origin story!

## Features

- Generate unique pet names based on pet type, personality, and quirks
- Each name comes with a mystically generated "origin story"
- Save your favorite names to a "pet registry"
- View your saved pet names and their lore

## Installation

1. Clone this repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies (if any):
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Generate a Pet Name

```bash
./pet_oracle.py generate --pet-type TYPE --personality PERSONALITY [--quirks QUIRK1 QUIRK2 ...] [--save]
```

Parameters:
- `--pet-type`, `-t`: Type of pet (dog, cat, bird, fish, reptile, rodent, other)
- `--personality`, `-p`: Pet's personality (playful, lazy, fierce, shy, curious, loving, grumpy)
- `--quirks`, `-q`: Optional unique quirks or traits of your pet (space-separated)
- `--save`, `-s`: Optional flag to save the generated name to the registry
- `--registry`, `-r`: Path to registry file (default: pet_registry.json)

Example:
```bash
./pet_oracle.py generate --pet-type cat --personality curious --quirks "sleeps upside-down" "chirps at birds" --save
```

### List Saved Pets

```bash
./pet_oracle.py list
```

## Examples

```
🔮 The Pet Name Oracle is channeling mystical energies... 🔮

✨ The Oracle reveals the name: Captain Pounce ✨

Origin Story:
In the ancient era, Captain Pounce was revered as a symbol of patience and charm.
```

## License

Open source - Feel free to use and modify!