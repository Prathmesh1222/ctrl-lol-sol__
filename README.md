# CTRL + LOL 😂

> **The Ultimate Online Meme Competition** by **Stats O'Locked**
> _Where Data Meets Memes_

[![Live Event](https://img.shields.io/badge/Event-Feb%2021--27%202026-blueviolet?style=for-the-badge)](https://github.com/Prathmesh1222/ctrl-lol)
[![Platform](https://img.shields.io/badge/Platform-Online-green?style=for-the-badge)](https://github.com/Prathmesh1222/ctrl-lol)
[![Built With](https://img.shields.io/badge/Built%20With-Flask%20%2B%20HTML%2FCSS%2FJS-orange?style=for-the-badge)](https://github.com/Prathmesh1222/ctrl-lol)

---

## 🧾 About

**CTRL + LOL** is a fully online meme creation competition running from **Feb 21 – 27, 2026**. Participants post memes on Instagram, tag our page, and the community votes through likes. Winners are determined by a mix of engagement (likes) and jury scoring.

---

## 🎯 How It Works

1. **Register** via the Google Form shared on our Instagram
2. **Create** a meme based on one of the 4 themes
3. **Post** it on Instagram and **tag `@statsol`**
4. We **upload approved memes** to this site daily
5. **Leaderboard** updates every 24 hrs based on likes + jury score

---

## 🗂️ Themes

| #   | Theme                 | Description                             |
| --- | --------------------- | --------------------------------------- |
| 01  | 🤖 Tech Life          | Windows updates, dark mode addiction    |
| 02  | 🐛 Coding Struggles   | Missing semicolons, StackOverflow fails |
| 03  | 🎓 College Chaos      | 8 AM classes, proxy attendance          |
| 04  | 💼 Placement Pressure | Aptitude tests, rejection emails        |

---

## 📊 Scoring

| Component  | Weight | Details                          |
| ---------- | ------ | -------------------------------- |
| Engagement | 50%    | 1 Instagram Like = 10 Points     |
| Jury Score | 50%    | Creativity, Relatability & Humor |

Leaderboard updates daily. Final results announced **Feb 27**.

---

## 🛠️ Tech Stack

- **Frontend:** HTML5, CSS3 (custom design system), Vanilla JS
- **Backend:** Python (Flask)
- **Storage:** CSV (submissions), JSON (posters metadata)
- **APIs:**
  - `GET /api/leaderboard` — Ranked submission data
  - `GET /api/memes` — Approved meme gallery
  - `GET /api/posters` — Event poster list
  - `POST /upload-poster` — Admin poster upload (PIN protected)
  - `POST /api/verify-pin` — Admin PIN verification

---

## 🚀 Running Locally

```bash
# 1. Clone the repo
git clone https://github.com/Prathmesh1222/ctrl-lol.git
cd ctrl-lol

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the server
python3 app.py
```

Then open: **http://localhost:5000**

---

## 📁 Project Structure

```
ctrl-lol/
├── app.py              # Flask backend
├── index.html          # Main website
├── styles.css          # All styling
├── script.js           # Frontend logic
├── requirements.txt    # Python dependencies
├── submissions.csv     # Meme submissions log
├── uploads/            # Uploaded memes & posters
│   └── posters/        # Event poster images
└── sol-logo.png        # Stats O'Locked logo
```

---

## 🔐 Admin Access

The **Poster Admin Panel** is accessible at the bottom of the site.

- PIN is set in `app.py` → `ADMIN_PIN`
- Admins can upload event posters which appear in the Event Posters gallery

---

## 📸 Follow Us

Instagram: [@statsol](https://instagram.com/statsol)

---

_Made with ☕ and Panic — Stats O'Locked © 2026_
