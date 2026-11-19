# 🌿 EcoSort | Smart Waste Guide
 
**EcoSort** is a desktop application that helps people identify waste correctly, find the nearest suitable dustbin, and build greener daily habits. Users earn Eco Points by checking items and taking quizzes, and can track their progress on a personal dashboard.
 
![Dashboard](screenshots/01-dashboard.png)
 
---
 
## Table of Contents
 
- [Features](#features)
- [Screenshots](#screenshots)
- [Getting Started](#getting-started)
- [How to Use](#how-to-use)
- [Eco Points and Levels](#eco-points-and-levels)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Known Limitations](#known-limitations)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)
---
 
## Features
 
| Feature | Description |
|---|---|
| **Dashboard** | Shows total Eco Points, items checked, categories found, progress towards the next milestone, and a daily eco tip. |
| **Waste Checker** | Type an item and get its waste category and disposal guidance, with suggestions as you type. |
| **Waste Directory** | Browse all supported items (14 at present), search by name, or filter by category. |
| **Find Bins** | Interactive map of nearby dustbins, filterable by waste type or item and sorted by distance. |
| **Bin Details** | Each bin shows its distance, accepted waste types, and a photo for easy recognition. |
| **Directions** | One click opens walking directions to the selected bin in Google Maps. |
| **Community Bins** | Add a dustbin you found, or remove one that no longer exists. |
| **Daily Challenge** | A new green challenge every day to build better habits. |
| **Eco Tips** | A list of simple, practical tips for a more eco-conscious lifestyle. |
| **Recycling Quiz** | Answer questions to test your knowledge and earn Eco Points. |
 
### Waste categories
 
`Recyclable Waste` · `Organic Waste` · `Hazardous Waste` · `E-Waste` · `Special Waste`
 
---
 
## Screenshots
 
### 1. Dashboard
Overview of your progress, with Eco Points, items checked, categories found, and a daily eco tip.
 
![Dashboard](screenshots/01-dashboard.png)
 
### 2. Waste Checker
Enter an item and see suggestions as you type.
 
![Waste Checker](screenshots/02-waste-checker.png)
 
### 3. Waste Directory
Browse supported items and filter them by category.
 
![Waste Directory](screenshots/03-waste-directory.png)
 
### 4. Find Bins Nearby
All nearby bins are shown on the map. Right-click to set your location or add a dustbin.
 
![Find Bins](screenshots/04-find-bins.png)
 
### 5. Filter Bins by Waste Type
Enter a waste type or item to see only the bins that accept it, nearest first.
 
![Filter Bins](screenshots/05-filter-bins.png)
 
### 6. Bin Details and Photos
View a photo of the bin, get directions, or remove the bin.
 
![Bin Details](screenshots/06-bin-details.png)
 
### 7. Directions on Google Maps
Walking directions open in Google Maps with the route already filled in.
 
![Google Maps Directions](screenshots/07-google-maps-directions.png)
 
### 8. Daily Challenge
A fresh green challenge each day.
 
![Daily Challenge](screenshots/08-daily-challenge.png)
 
### 9. Eco Tips
Practical tips for greener living.
 
![Eco Tips](screenshots/09-eco-tips.png)
 
### 10. Recycling Quiz
Answer questions to earn Eco Points.
 
![Recycling Quiz](screenshots/10-recycling-quiz.png)
 
### 11. Earning Points with the Waste Checker
Checking an item earns points and links straight to the nearest suitable bin.
 
![Waste Checker Points](screenshots/11-checker-points.png)
 
### 12. Updated Dashboard
The dashboard updates automatically as you earn points.
 
![Updated Dashboard](screenshots/12-dashboard-points.png)
 
---
 
## Getting Started
 
### Prerequisites
 
- Python 3.x
- An internet connection (needed for map tiles and Google Maps directions)
### Installation
 
> ⚠️ Update the commands below to match your project (repository name, entry file, dependency list).
 
```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
 
# 2. (Optional) Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux
 
# 3. Install dependencies
pip install -r requirements.txt
 
# 4. Run the app
python main.py
```
 
---
 
## How to Use
 
1. **Check an item.** Open **Waste Checker**, type an item (for example, *newspaper*), and select **Identify waste**. You earn Eco Points and see its category and disposal guidance.
2. **Find a bin.** Select **Find nearest bin for this waste**, or open **Find Bins** directly.
3. **Set your location.** Use **Detect my location**, enter coordinates, or right-click the map and choose **Set my location here**.
4. **Pick a bin.** Choose a bin from the list or the map to see its photo and distance, then select **Get directions** to open Google Maps.
5. **Add or remove bins.** Right-click the map and choose **Add dustbin here**, or use **Add a dustbin I found**. Use **Remove this bin** if a bin no longer exists.
6. **Build habits.** Try the **Daily Challenge**, read the **Eco Tips**, and take the **Recycling Quiz** to earn more points.
---
 
## Eco Points and Levels
 
| Action | Points |
|---|---|
| Identify a waste item | +5 |
| Answer a quiz question correctly | +10 |
 
| Level | Progress |
|---|---|
| Eco Beginner | Starting level (0 / 20 points to the next milestone) |
| Green Champion | Reached by earning more points (30 / 50 towards the next milestone) |
 
> Update this table if your point values or level thresholds change.
 
---
 
## Tech Stack
 
> ⚠️ Fill in the technologies you actually used.
 
- **Language:** Python
- **Interface:** `<GUI / web view framework>`
- **Maps:** OpenStreetMap-based map `<library, e.g. Leaflet>`
- **Directions:** Google Maps (opens in the browser)
- **Data storage:** `<JSON / SQLite / other>`
---
 
## Project Structure
 
> ⚠️ Replace with your real folder layout.
 
```
<repo-name>/
├── main.py
├── requirements.txt
├── data/
├── assets/
├── screenshots/
├── README.md
└── LICENSE
```
 
---
 
## Known Limitations
 
- The waste directory currently supports only 14 items.
- Disposal guidance is general. Collection rules vary by city and locality, so always check your local rules.
- Bins added by users are not verified, and any user can remove a bin.
---
 
## Roadmap
 
- [ ] Expand the waste directory and add fuzzy search for misspelled items
- [ ] Require a name for every bin and ask for confirmation before removing one
- [ ] Limit how often points can be earned, to stop repeated farming
- [ ] Add a "Mark as done" button and streak counter for daily challenges
- [ ] Add local disposal rules, such as wet and dry waste segregation
---
 
## Contributing
 
Contributions are welcome.
 
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push the branch: `git push origin feature/your-feature`
5. Open a Pull Request
---
 
## License
 
This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.
 
---
 
## Acknowledgements
 
- Map data © [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors
- Directions provided by [Google Maps](https://maps.google.com)
*Small steps matter. Make today a little greener.* 🌱
 
