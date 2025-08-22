# NEST

## Team: It Takes Five
1. Jitao Zhang
2. Joanne Chien
3. Venkata Surya Sai Nikhil Garimella
4. Harsh Pinge
5. Sharon Xiao

---

## Purpose of this application
A group of MMA students just graduated. After a hardworking year of study, the class decides to take a vacation together. 
They have a budget and know what kind of environments they want to be greeted.
With their analytics background, they want to find their dream property using a data-driven way. 
This app helps them find their best match.

## What does this application do?
Nest is a Python-based application that simulates an **Airbnb-like property search and recommendation system**.  
It allows users to create profiles, set their travel preferences (destination, budget, group size, environments, features), and get matched with the most suitable properties.  

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
    "name": "Carrot",
    "destination": "Krakow",
    "group_size": 3,
    "budget": 600,
    "preferred_environment": ["garden view", "quiet"],
    "features": ["wifi", "refrigerator"]
  }
  ```
- Top Match Output

| Property ID | Location | Nightly Price | Environ                                                                                | Features                                                          | Score |
|-------------|----------|---------------|----------------------------------------------------------------------------------------|-------------------------------------------------------------------|-------|
| 1           | Krakow   | 541           | [garden view, village, luxury, lake house]                                             | [Refrigerator, Pets Allowed]                                      | 80    |
| 185         | Krakow   | 389           | [family-friendly, boutique, gardens]                                                   | [Washer/Dryer, Dog-Friendly, Air Conditioning, Gym, Beach Access] | 76    |
| 423         | Krakow   | 389           | [hillside, forest, mountain view, family-friendly, village, beach access, lake access] | [Patio, Beach Access, Gym, Parking]                               | 76    |

  
- LLM Suggested Activities 
  ```markdown
   Property ID 1 in Krakow:
   - Enjoy a leisurely boat ride or fishing on the nearby lake
   - Explore the charming village and its local markets
   - Have a relaxing picnic in the garden with a view
  
   Property ID 185 in Krakow:
   - Spend a fun day at the beach with family and pets
   - Take a walk through the boutique gardens and enjoy the scenery
   - Visit local family-friendly attractions in Krakow

   Property ID 423 in Krakow:
   - Go hiking in the nearby forest and hillside trails
   - Enjoy water activities like swimming or kayaking at the lake
   - Have a BBQ on the patio with mountain views
  
  ```

## Troubleshooting 
- `ValueError: No content returned from the API!`
  - Check API key and model name in `PropertyPoolGenertor.py`
- `json.decoder.JSONDecodeError`
  - The LLM sometimes returns invalid JSON; the script reties automatically.
- `401 Unauthorized`
  - Ensure your OpenRouter API key is active and correct.

