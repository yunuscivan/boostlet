# Boostlet – Intelligent Resource Optimizer 
## ( including its website )

Boostlet is a lightweight desktop utility that helps users regain system performance when CPU and RAM usage gets high.  It's designed to act only when necessary, not to run permanently in the background. ( now only the Windows version ) Downloadable from its website !

While working in e-commerce, I was looking for a solution to frequent slowdowns on my computer. I developed Boostlet for the personal project assignment in Powercoders Bootcamp thinking about this problem — using basic Python knowledge, open-source resources, and AI tools such as ChatGPT, Microsoft Copilot, and DeepSeek.

Boostlet can be useful on devices in certain situations:

Systems with 8 GB RAM or more that have been running for hours, PCs frequently using heavy browsers (e.g., Chrome with many tabs) or background tools, office laptops running multiple apps (Teams, Excel, Outlook, etc.) simultaneously, developers’ machines using IDEs, emulators or virtual machines, any system experiencing gradual slowdown over time due to memory fragmentation.

To download it : http://www.boostlet.app/ 

## How It Works

1. Boostlet monitors CPU and RAM usage.
2. When user-defined thresholds are exceeded:
   - It either alerts the user, or cleans RAM automatically. ( and the user can also add deep Ram cleaning )*
3. The cleaning process trims memory from running processes (working sets).
* Optional: It performs deep cleaning using an external tool (`EmptyStandbyList.exe`) to release cached memory.

---

## Key Features

- **Manual & Automatic Cleaning: Clean memory with one click ( on the window or on system tray in Windows ), or let Boostlet react automatically when usage thresholds are exceeded.
- **Deep RAM Cleaning: Optionally frees cached and standby memory for deeper optimization, additionally. 
- **Threshold-Based Triggers: Set custom CPU and RAM thresholds that define when Boostlet should act.
- **Interval Mode: Schedule RAM cleanup every X minutes, acting like an automatic background cleaner.
- **System Info View: Displays CPU model, OS, RAM amount, and uptime.
- **Tray Mode: Keep Boostlet active in the background with right-click tray access.

---

### Technologies Used

| Technology / Library         | Description                                                               |
|-----------------------------|---------------------------------------------------------------------------|
| Python                      | Main programming language                                                 |
| PySide6 (Python library)    | GUI development                                    |
| psutil (Python library)     | Accesses real-time CPU and RAM usage statistics                           |
| ctypes (Standard module)    | Calls Windows APIs to clean working sets     |
| subprocess (Standard module)| Executes external tools like `EmptyStandbyList.exe`                       |
| platform (Standard module)  | Retrieves OS and hardware information                                     |
| json (Standard module)      | Stores and loads user settings from local configuration files             |
| time (Standard module)      | Tracks system uptime and manages delays                                   |
| PyInstaller                 | Packages the application into a standalone Windows `.exe`                 |
| NSIS (Nullsoft Installer)   | Used to build the installer for full deployment (in website folder)       |


## Interface Overview

### Main Window
- Set CPU/RAM thresholds
- Choose between:
  -  Alert mode (ask before cleaning)
  -  Auto-clean mode (clean directly)
- Enable deep cleaning and interval cleaning
- View current CPU and RAM usage
- Access system info
- Click “Clean RAM Now” any time

### Tray Menu
- Show/hide window
- Clean RAM instantly
- Exit application

> Tip: “Clean RAM Now” works even if neither Alert nor Auto-clean is selected.

---

## Recommended Settings

- Set CPU and RAM thresholds to ~80%
- Use Alert Mode if you prefer manual control
- Use Auto-clean Mode for hands-free optimization
- Use Interval Mode for scheduled maintenance (disables thresholds)

---

## Ram Cleaning and How

Boostlet uses Python's ctypes module to call Windows API functions that empty the working sets of running processes.Working sets are portions of a process's memory that are currently resident in physical RAM.

When a process does not use some of its memory pages frequently, those pages can be pushed out (cleaned) from RAM, freeing up space for other active processes.

It requires administrator privileges.

### What is `EmptyStandbyList.exe`? ( Deep Ram Cleaning Feature )

`EmptyStandbyList.exe` is a lightweight utility used to clear the standby memory list on Windows systems. Standby memory consists of cached pages that are no longer actively in use but are still held in RAM.

Boostlet uses this tool optionally when Deep RAM Cleaning is enabled. It requires administrator privileges.

This tool is open-source and originally provided by Wj32 (https://wj32.org/wp/software/empty-standby-list/). It is included in Boostlet for convenience and transparency.

## The Website

The Boostlet website is designed as a simple and responsive static site to present and support the Boostlet application. It was built using the following technologies:

- HTML files and CSS files (2 different style sheets) : Used for the structure and visual styling of all pages, giving the website a clean, modern look with a consistent layout and color theme.
- PHP (feedback.php): Used to handle the contact form. When a user submits feedback via the `feedback.html` page, the form data (name, email, and message) is processed by a PHP script that sends the information directly to the developer’s email address. This allows for easy user interaction without needing a full backend framework.

- `index.html` – It provides a short introduction to Boostlet, lists key features, and includes the Windows installer download link.
- `guide.html` – A documentation page that explains how to use Boostlet, recommended settings, and what each option does.
- `feedback.html` – A simple contact form where users can enter their name, email, and message. It is connected to the PHP script mentioned above (`feedback.php`) to deliver submissions to the developer.
- `about.html` – A short bio of the developer with a link to the personal website.

The website www.boostlet.app is hosted on Hostinger and maintained using its web-based file manager. This allows quick manual updates by editing HTML, CSS, and PHP files directly.


### Folder Structure

```text
Boostlet/
├── boostlet.py             # Main application code
├── boostlet.exe            # The .exe format 
├── boostlet.ico            # App icon
├── EmptyStandbyList.exe    # Deep RAM cleaner 
├── boostlet_settings.json  # Saved user settings
├── website/                # Website files (www.boostlet.app)
│   ├── index.html
│   ├── guide.html
│   ├── about.html
│   ├── feedback.html
│   └── ...

```

⚠️ Important Note:  
> If you run the `.exe` file directly (e.g. from GitHub or by copying it alone), the system tray icon may not appear correctly when clicking "Close Window" or "Close" — because the icon file (`boostlet.ico`) is missing.  
> For full functionality (especially tray visibility), make sure to keep the `.exe` file together with all related assets (like the icon file) in the same directory.


I hope you liked the app and its website! Do not forget to send your feedback on the website ! And this is the very first version of the tool, I am planing to add another features like being able to see the apps, which have the highest CPU and RAM load ( and also with a kill function maybe ) and more ! The MacOS and mobile versions are coming soon...Thanks!
