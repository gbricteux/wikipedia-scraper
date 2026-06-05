# wikipedia-scraper
[![forthebadge made-with-python](https://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)


## 🏢 Description

This project aims to request leaders per countries from the database (https://country-leaders.onrender.com/) and append to the leader's description the first paragraph of their wikipedia page.

The descriptions of the leaders are stored in a json file.

## 📦 Repo structure

```
.
├── dev/
|  ├── gaetan_sandbox_notebook.ipynb
│  ├── hussein_sandbox_notebook.ipynb
├── src/
|  ├── __init__.py
│  ├── api_client.py
│  └── html_scraper.py
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
```

## 🛎️ Usage

1. Clone the repository to your local machine.

2. To run the script, you can execute the `main.py` file from your command line:

```
   python main.py
```

3. The script requests several countries from the database and then the leaders of each country. It then requests the first paragraph of the wikipedia page of the leaders in their own language. The wikipedia text is stored in the leaders description. The leaders decriptions are stored in a json format in file *leaders.json*.

## ⏱️ Timeline

This project took three days for completion.

## 📌 Personal Situation
This project was done as part of the AI Boocamp at BeCode.org by 2 contributors : Gaetan Bricteux ([LinkedIn](https://www.linkedin.com/in/gaëtan-bricteux)) and Hussein Abuammar ([LinkedIn](https://www.linkedin.com/in/hussein-abuammar)).
