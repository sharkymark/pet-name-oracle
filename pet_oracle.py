#!/usr/bin/env python3
"""
Pet Name Oracle - A mystical generator of pet names based on pet type, personality, and user quirks.
Includes an origin story for each name using a templated lore generator.
Names can be saved to a "pet registry" file.
"""

import random
import json
import os
import argparse
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Constants
DEFAULT_REGISTRY_PATH = "pet_registry.json"

# Name components by pet type
NAME_COMPONENTS = {
    "dog": {
        "prefixes": ["Sir", "Captain", "Duke", "Lady", "Professor", "Baron", "Duchess", "King", "Queen", "Lord"],
        "bases": ["Bark", "Woof", "Paw", "Sniff", "Fetch", "Wag", "Fluff", "Spot", "Scout", "Buddy"],
        "suffixes": ["ington", "ster", "ums", "y", "ie", "er", "son", "o", "a", "paws"]
    },
    "cat": {
        "prefixes": ["Mr.", "Ms.", "Professor", "Count", "Dr.", "Emperor", "Empress", "Prince", "Princess", "Whisker"],
        "bases": ["Purr", "Meow", "Whisker", "Pounce", "Claw", "Scratch", "Nap", "Shadow", "Fluff", "Mittens"],
        "suffixes": ["ton", "kins", "y", "ie", "er", "paws", "fur", "tail", "bean", "whiskers"]
    },
    "bird": {
        "prefixes": ["Captain", "Wing", "Sky", "Cloud", "Feather", "Sir", "Madam", "Air", "Chirp", "Flutter"],
        "bases": ["Tweet", "Chirp", "Squawk", "Flap", "Soar", "Beak", "Wing", "Feather", "Plume", "Sing"],
        "suffixes": ["song", "beak", "wings", "sky", "er", "ie", "y", "oo", "ster", "ington"]
    },
    "fish": {
        "prefixes": ["Bubble", "Captain", "Sir", "Madam", "Admiral", "Splash", "Wave", "Coral", "Aqua", "Fin"],
        "bases": ["Swim", "Splash", "Gill", "Fin", "Bubble", "Ripple", "Scale", "Wave", "Coral", "Pearl"],
        "suffixes": ["scale", "fin", "bubbles", "gills", "ie", "y", "o", "er", "swimmer", "fish"]
    },
    "reptile": {
        "prefixes": ["Sir", "Captain", "Scale", "Cold", "Sun", "Ancient", "Prime", "Royal", "Master", "Dr."],
        "bases": ["Scale", "Slither", "Claw", "Fang", "Shell", "Cold", "Bask", "Snap", "Crunch", "Hiss"],
        "suffixes": ["claw", "scale", "fang", "shell", "ie", "y", "o", "er", "tail", "tooth"]
    },
    "rodent": {
        "prefixes": ["Tiny", "Squeaky", "Sir", "Miss", "Little", "Quick", "Whisker", "Nibble", "Scurry", "Fuzzy"],
        "bases": ["Squeak", "Scamper", "Nibble", "Cheek", "Whisker", "Fuzzy", "Tiny", "Scurry", "Pebble", "Puff"],
        "suffixes": ["puff", "cheeks", "tail", "whiskers", "ie", "y", "er", "kins", "nibbles", "squeaker"]
    },
    "other": {
        "prefixes": ["Sir", "Madam", "Captain", "Professor", "Dr.", "Master", "Royal", "Supreme", "Ultra", "Mega"],
        "bases": ["Cuddle", "Snuggle", "Friend", "Buddy", "Pal", "Wonder", "Amazo", "Mystical", "Cosmic", "Majestic"],
        "suffixes": ["ton", "ster", "io", "ius", "ella", "ington", "paws", "heart", "soul", "legend"]
    }
}

# Personality traits influence name components
PERSONALITY_TRAITS = {
    "playful": {
        "prefixes": ["Bouncy", "Fun", "Happy", "Zippy", "Jolly"],
        "bases": ["Play", "Jump", "Bounce", "Wiggle", "Giggle"],
        "suffixes": ["jumps", "zoomies", "fun", "joy", "smile"]
    },
    "lazy": {
        "prefixes": ["Sleepy", "Dozy", "Nappy", "Drowsy", "Cozy"],
        "bases": ["Snooze", "Nap", "Yawn", "Dream", "Lazy"],
        "suffixes": ["snooze", "dreams", "pillow", "naps", "zzz"]
    },
    "fierce": {
        "prefixes": ["Mighty", "Fearsome", "Savage", "Warrior", "Battle"],
        "bases": ["Fang", "Claw", "Snarl", "Growl", "Fight"],
        "suffixes": ["fang", "claw", "fury", "warrior", "beast"]
    },
    "shy": {
        "prefixes": ["Timid", "Quiet", "Gentle", "Soft", "Whisper"],
        "bases": ["Hide", "Peek", "Whisper", "Soft", "Gentle"],
        "suffixes": ["shadow", "corner", "quiet", "shy", "whisper"]
    },
    "curious": {
        "prefixes": ["Wonder", "Curious", "Nosy", "Explorer", "Seeker"],
        "bases": ["Peek", "Poke", "Snoop", "Seek", "Quest"],
        "suffixes": ["finder", "seeker", "explorer", "wander", "quest"]
    },
    "loving": {
        "prefixes": ["Sweet", "Lovely", "Cuddle", "Huggy", "Heart"],
        "bases": ["Love", "Cuddle", "Snuggle", "Heart", "Kiss"],
        "suffixes": ["heart", "love", "hugs", "kisses", "sweetheart"]
    },
    "grumpy": {
        "prefixes": ["Grumpy", "Grouchy", "Cranky", "Fussy", "Moody"],
        "bases": ["Grump", "Scowl", "Frown", "Grumble", "Huff"],
        "suffixes": ["grump", "scowls", "frowns", "grouch", "grumbler"]
    }
}

# Lore templates for origin stories
LORE_TEMPLATES = [
    "Legend says {name} was born under a {celestial_body} on the {nth} day of {season}, blessed with the power of {power}.",
    "In ancient times, {name} was the guardian of {place}, protecting it with the mystical gift of {power}.",
    "Whispered among the {people}, {name} is said to possess the rare ability to {ability} when the {event} occurs.",
    "From the distant lands of {place}, {name} journeyed across {terrain} carrying the sacred {item}.",
    "{name} was once the companion of a great {profession}, granting them the wisdom to {achievement}.",
    "Scholars believe {name} is the reincarnation of {historical_figure}, returned to bring {gift} to the world.",
    "The prophecy of {prophet} foretold that {name} would appear during the {event} to {mission}.",
    "Born from a {element} storm, {name} carries the essence of {essence} within their soul.",
    "In the {time_period} era, {name} was revered as a symbol of {virtue} and {quality}.",
    "The secret society of {society} named {name} after their founder who discovered the art of {art}."
]

# Lore template filling components
LORE_COMPONENTS = {
    "celestial_body": ["full moon", "blue star", "red comet", "eclipse", "northern lights", "cosmic alignment"],
    "nth": ["first", "second", "third", "seventh", "ninth", "thirteenth", "final"],
    "season": ["spring", "summer", "autumn", "winter", "harvest", "solstice", "equinox"],
    "power": ["invisibility", "dream-walking", "healing", "foresight", "speaking with ancestors", "time-bending"],
    "place": ["Whisker Woods", "Mystic Mountain", "Paw Valley", "Ancient Ruins", "Crystal Cave", "Enchanted Lake"],
    "people": ["elders", "forest dwellers", "mountain sages", "ancient scholars", "mystical creatures", "nomadic tribes"],
    "ability": ["find lost treasures", "predict storms", "bring good fortune", "heal broken hearts", "speak ancient tongues", "see the future"],
    "event": ["great conjunction", "midnight hour", "lunar eclipse", "summer solstice", "autumn winds", "spring bloom"],
    "terrain": ["vast deserts", "treacherous mountains", "endless oceans", "dense forests", "frozen tundras", "mystical realms"],
    "item": ["orb of knowledge", "scroll of wisdom", "crystal of truth", "feather of flight", "gem of power", "seed of life"],
    "profession": ["wizard", "warrior", "healer", "scholar", "ruler", "explorer", "bard", "sage"],
    "achievement": ["build wonders", "end wars", "unite kingdoms", "discover hidden knowledge", "create magic", "achieve immortality"],
    "historical_figure": ["great ruler", "wise sage", "legendary hero", "mystical enchanter", "divine being", "ancient protector"],
    "gift": ["peace", "wisdom", "prosperity", "harmony", "healing", "enlightenment", "joy", "protection"],
    "prophet": ["whiskers", "feathers", "scales", "ancient one", "dreamer", "star gazer", "moon watcher", "truth speaker"],
    "mission": ["restore balance", "bring peace", "share knowledge", "protect the innocent", "ensure prosperity", "spread joy"],
    "element": ["fire", "water", "earth", "air", "lightning", "shadow", "light", "star"],
    "essence": ["courage", "wisdom", "love", "strength", "patience", "kindness", "loyalty", "resilience"],
    "time_period": ["ancient", "medieval", "golden", "silver", "bronze", "forgotten", "remembered", "prophesied"],
    "virtue": ["courage", "wisdom", "patience", "honesty", "kindness", "loyalty", "perseverance", "compassion"],
    "quality": ["strength", "intelligence", "grace", "beauty", "agility", "resilience", "charm", "mystery"],
    "society": ["midnight prowlers", "dawn seekers", "celestial observers", "dream walkers", "whisper keepers", "paw prints"],
    "art": ["dream walking", "star reading", "future seeing", "joy bringing", "soul soothing", "heart healing"]
}

def generate_pet_name(pet_type: str, personality: str, quirks: List[str]) -> str:
    """Generate a pet name based on pet type, personality, and quirks."""
    # Default to "other" if pet type not found
    if pet_type not in NAME_COMPONENTS:
        pet_type = "other"
    
    # Default to a random personality if not found
    if personality not in PERSONALITY_TRAITS:
        personality = random.choice(list(PERSONALITY_TRAITS.keys()))
    
    # Combine base components with personality influence
    prefix_pool = NAME_COMPONENTS[pet_type]["prefixes"] + PERSONALITY_TRAITS[personality]["prefixes"]
    base_pool = NAME_COMPONENTS[pet_type]["bases"] + PERSONALITY_TRAITS[personality]["bases"]
    suffix_pool = NAME_COMPONENTS[pet_type]["suffixes"] + PERSONALITY_TRAITS[personality]["suffixes"]
    
    # Allow quirks to influence name (add random words based on quirks)
    for quirk in quirks:
        if quirk and len(quirk.strip()) > 0:
            # Sanitize quirk and use it as influence
            quirk_word = quirk.strip().split()[0].capitalize()
            if len(quirk_word) > 3:
                if random.random() < 0.3:  # 30% chance to incorporate directly
                    if random.random() < 0.5:
                        prefix_pool.append(quirk_word)
                    else:
                        base_pool.append(quirk_word)
    
    # Generate name parts
    name_structure = random.choice([
        "{prefix} {base}{suffix}",
        "{prefix} {base}",
        "{base}{suffix}",
        "{prefix}{base}",
        "{base} {suffix}",
        "{prefix} {base} {suffix}"
    ])
    
    # Select components
    prefix = random.choice(prefix_pool) if "{prefix}" in name_structure else ""
    base = random.choice(base_pool) if "{base}" in name_structure else ""
    suffix = random.choice(suffix_pool) if "{suffix}" in name_structure else ""
    
    # Assemble name
    name = name_structure.format(prefix=prefix, base=base, suffix=suffix)
    return name.strip()

def generate_lore(name: str) -> str:
    """Generate a mystical origin story for the pet name."""
    # Select a random lore template
    template = random.choice(LORE_TEMPLATES)
    
    # Fill in the template with random components
    lore = template.format(
        name=name,
        **{comp: random.choice(options) for comp, options in LORE_COMPONENTS.items()}
    )
    
    return lore

def save_to_registry(pet_info: Dict, registry_path: str = DEFAULT_REGISTRY_PATH) -> None:
    """Save the pet name and lore to the registry file."""
    # Load existing registry or create new one
    if os.path.exists(registry_path):
        try:
            with open(registry_path, 'r') as f:
                registry = json.load(f)
        except json.JSONDecodeError:
            # If file exists but is not valid JSON, start fresh
            registry = []
    else:
        registry = []
    
    # Add timestamp to pet info
    pet_info["created_at"] = datetime.now().isoformat()
    
    # Add new entry
    registry.append(pet_info)
    
    # Save updated registry
    with open(registry_path, 'w') as f:
        json.dump(registry, f, indent=2)
    
    print(f"Pet saved to registry at {registry_path}")

def display_registry(registry_path: str = DEFAULT_REGISTRY_PATH) -> None:
    """Display all pets in the registry."""
    if not os.path.exists(registry_path):
        print("Registry does not exist yet. Create a pet first!")
        return
    
    try:
        with open(registry_path, 'r') as f:
            registry = json.load(f)
        
        if not registry:
            print("Pet registry is empty. Create a pet first!")
            return
        
        print("\n=== 🐾 PET REGISTRY 🐾 ===")
        for i, pet in enumerate(registry, 1):
            print(f"\n{i}. {pet['name']} - {pet['pet_type'].capitalize()}")
            print(f"   Personality: {pet['personality'].capitalize()}")
            print(f"   Quirks: {', '.join(pet['quirks'])}")
            print(f"   Created: {pet['created_at']}")
            print(f"   Lore: {pet['lore']}")
        
        print("\n=========================")
    
    except (json.JSONDecodeError, KeyError):
        print("Error reading registry. The file may be corrupted.")

def main() -> None:
    """Main function to run the Pet Name Oracle CLI."""
    parser = argparse.ArgumentParser(description="Pet Name Oracle - Generate mystical pet names with lore")
    
    # Command subparsers
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Generate command
    generate_parser = subparsers.add_parser("generate", help="Generate a new pet name")
    generate_parser.add_argument("--pet-type", "-t", required=True, 
                                help="Type of pet (dog, cat, bird, fish, reptile, rodent, other)")
    generate_parser.add_argument("--personality", "-p", required=True,
                                help="Pet's personality (playful, lazy, fierce, shy, curious, loving, grumpy)")
    generate_parser.add_argument("--quirks", "-q", nargs="+", default=[],
                                help="Unique quirks or traits of your pet (space-separated)")
    generate_parser.add_argument("--save", "-s", action="store_true",
                                help="Save the generated name to the registry")
    generate_parser.add_argument("--registry", "-r", default=DEFAULT_REGISTRY_PATH,
                                help=f"Path to registry file (default: {DEFAULT_REGISTRY_PATH})")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List all pets in the registry")
    list_parser.add_argument("--registry", "-r", default=DEFAULT_REGISTRY_PATH,
                            help=f"Path to registry file (default: {DEFAULT_REGISTRY_PATH})")
    
    args = parser.parse_args()
    
    # Handle commands
    if args.command == "generate":
        print("🔮 The Pet Name Oracle is channeling mystical energies... 🔮\n")
        
        # Generate name and lore
        name = generate_pet_name(args.pet_type.lower(), args.personality.lower(), args.quirks)
        lore = generate_lore(name)
        
        # Display results
        print(f"✨ The Oracle reveals the name: {name} ✨")
        print(f"\nOrigin Story:\n{lore}\n")
        
        # Save to registry if requested
        if args.save:
            pet_info = {
                "name": name,
                "pet_type": args.pet_type.lower(),
                "personality": args.personality.lower(),
                "quirks": args.quirks,
                "lore": lore
            }
            save_to_registry(pet_info, args.registry)
    
    elif args.command == "list":
        display_registry(args.registry)
    
    else:
        # Default behavior if no command is provided
        parser.print_help()

if __name__ == "__main__":
    main()