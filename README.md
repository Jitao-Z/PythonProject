# NEST

## Team: It Takes Five

1. Jitao Zhang
2. Joanne Chien
3. Venkata Surya Sai Nikhil Garimella
4. Harsh Pinge
5. Sharon Xiao

---

## Purpose of this application

A group of MMA students just graduated. After a hardworking year of study, the class decides to take a vacation
together.
They have a budget and know what kind of environments they want to be greeted.
With their analytics background, they want to find their dream property using a data-driven way.
This app helps them find their best match.

## What does this application do?

Nest is a Python-based application that simulates an **Airbnb-like property search and recommendation system**.
It focuses on North American travel destination only. 
It allows users to create profiles, set their travel preferences (destination, budget, group size, environments,
features), and get matched with the most suitable properties.

Additionally, it integrates with Large Language Models (LLM) (via OpenRouter API) to:

- Generate pools of locations, environments, and features.
- Suggest fun and relevant activities for matched properties.

---

## Features

- Create, view, edit, and delete user profiles.
- Store user data in `profiles.json` for persistence.
- Match users to properties based on:
    - Destination
    - Group size
    - Budget
    - Preferred environments
    - Desired features
- Use **scoring system** to rank properties and return top 5 matches.
- Integrate with LLMs to:
    - Generate datasets of property pools (`PropertyPoolGenerator.py`).
    - Suggest activities for top property recommendations.
- Save and reload user and property data automatically.

---

## Project Structure

Nest

```markdown
├── data/ # Storage for JSON datasets
│ ├── profiles.json # User profiles
│ ├── properties.json # Randomly generated properties based on the LLM generated pools
│ ├── ###TO BE DELETED### LLM_Generated_Properties.json # LLM generated property pool
│ └── testPropertyPool.json # LLM generated features/environ/locations
├── main.py # Entry point for the program
├── NestApp.py # Main application logic & menu
├── Property.py # Property class for property storage
├── PropertyPoolGenerator.py # LLM generator for property pools
├── RandomPropertyGenerator.py # Random dataset generator
├── User.py # User class that include actions for editing different user attributes
├── UserProfileManagement.py # User storage & management
└── README.md # Documentation (this file)
```

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Jitao-Z/PythonProject.git
   cd nest
   ```
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
    - Dependencies include:
        - `pandas`
        - `requests`
3. LLM Function Dependency
    - Get a free API key from OpenRouter.ai
    - You will be prompted to enter the key when running scripts that use LLMs

## Usage

Run the main application:

  ```bash
  python main.py
  ```

You will then see the following interactive menu:

  ```
  Please enter:
    1 to Add a user,
    2 to View a user,
    3 to Edit an existing profile,
    4 to Get recommended properties for an existing profile and (optional) to get suggested activities for your recommended properties,
    5 to Delete an existing user,
    6 to Exit.
  ```

Example workflow:

1. Add a user (`1`).
2. Get matched properties (`4`).
3. Optional: Use the LLM to generate suggestive activities for the matched properties (`y/n`)

## Scripts Overview

- ` main.py ` – Entry point; runs the app.
- ` NestApp.py ` – Core logic: user management, property matching, menu handling.
- ` Property.py ` – Property class for storing property attributes.
- ` User.py ` – User class for storing user preferences and methods for updates.
- ` UserProfileManagement.py ` – Manage user profiles, including: Loads, saves, adds, deletes, and searches for users.
- ` PropertyPoolGenerator.py ` – Uses LLM to generate property pools (locations, features, environments).
- ` RandomPropertyGenerator.py ` – Generates a large random property dataset for testing.

## Matching Algorithm

Each property is scored against a user's profile based on:

- Group Size Fit (30%)
- Budget Fit (30%)
- Environment Preferences (20%)
- Features Preferences (20%)
  Top 5 properties with the highest final scores are recommended.

## LLM Integration

The system uses OpenRouter API for:

1. Property Pool Generation
    - Generate a list of locations, features, and environments to build property datasets
2. Activity Suggestions
    - Given the top 5 matched properties, LLM suggests 3 fun and relevant activities for each property

Example

- User Profile
  ```json
  {
    "name": "Taylor",
    "destination": "Portland",
    "group_size": 2,
    "budget": 400,
    "preferred_environment": ["quiet", "cozy", "lakeside"],
    "features": ["wifi", "kitchen", "2 bedroom"]
  }
  ```
- Top Match Output

| Property ID | Location | Nightly Price | Environ                                                                                       | Features                                                                                                                                 | Score |
|-------------|----------|---------------|-----------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|-------|
| 1757        | Portland | 174           | [secluded, lakeside, historic home, golf course nearby, clifftop, vineyard, secluded cottage] | [shampoo and soap, outdoor furniture, pet friendly, breakfast included, sea view, fireplace, wifi, heating, air conditioning, game room] | 84    |
| 5430        | Portland | 136           | [castle, clifftop, wildlife viewing location, mountain, secluded cottage, secluded]           | [wifi, kitchen, smart tv, balcony, private parking, breakfast included, mountain view, bbq grill]                                        | 84    |
| 5907        | Portland | 153           | [waterfront, stroller accessible, clifftop]                                                   | [wifi, game room, city view, outdoor furniture, smart tv, heating, smoking allowed, dishwasher, mountain view, sofa]                     | 80    |
| 4035        | Portland | 150           | [dog-friendly, farm stay, mountain cabin]                                                     | [fireplace, gym, beds linens included, pet friendly, sofa, dishwasher, air conditioning, kitchen]                                        | 80    |
| 3969        | Portland | 225           | [wildlife viewing location, seaside, treehouse, farmhouse, island]                            | [kitchen, smoking allowed, towels included, mountain view, dishwasher, outdoor furniture, hot tub, balcony, sea view]                    | 80    |

- LLM Suggested Activities
  ```markdown
   Property ID 1757 in Portland:
   - Enjoy a peaceful lakeside picnic with scenic views
   - Play a round of golf at the nearby course
   - Explore the historic home and its surroundings for a glimpse into the past

   Property ID 5430 in Portland:
   - Take in breathtaking views from the clifftop castle
   - Go wildlife spotting in the secluded mountain area
   - Host a BBQ on the balcony with mountain vistas

   Property ID 5907 in Portland:
   - Relax by the waterfront with a book or a picnic
   - Challenge friends or family to games in the game room
   - Enjoy the city and mountain views from the clifftop location

   Property ID 4035 in Portland:
   - Take your dog for a hike in the surrounding mountain trails
   - Cozy up by the fireplace after a day of farm activities
   - Cook a farm-to-table meal using local produce in the kitchen

   Property ID 3969 in Portland:
   - Unwind in the hot tub while enjoying seaside views
   - Explore the island and its wildlife for a nature adventure
   - Have a relaxing evening on the balcony with a view of the sea

  ```

## Troubleshooting

- `ValueError: No content returned from the API!`
    - Check API key and model name in `PropertyPoolGenertor.py`
- `json.decoder.JSONDecodeError`
    - The LLM sometimes returns invalid JSON; the script reties automatically.
- `401 Unauthorized`
    - Ensure your OpenRouter API key is active and correct.

