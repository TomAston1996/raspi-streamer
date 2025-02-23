[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

# 📄 Raspberry Pi Streamer

The goal of this project is to extract performance metrics (such as CPU utilisation etc.) from a Raspberry Pi and feed it into AWS IoT Core.
IoT Core rules will publish events to AWS middleware which will in turn transform and store the data in DynamoDB. A simple FastAPI app will be hosted on ECS
for user access to the data.

## 🧑‍💻 Tech Stack

![Python]
![AWS]

## 🚀 Setup

This project uses [`uv`](https://github.com/astral-sh/uv) as the package manager for fast and reproducible environments.

### 🔧 **1. Install `uv` (if not installed)**
Make sure you have `uv` installed. If not, install it with:
```sh
pipx install uv
```
### 📦 2. Create & Sync the Virtual Environment
Run the following command to create and set up the virtual environment:
```sh
uv venv create .venv
uv sync
```

## 🧑‍🤝‍🧑 Developers 

| Name           | Email                      |
| -------------- | -------------------------- |
| Tom Aston      | mailto:mail@tomaston.dev     |

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/TomAston1996/raspi-streamer.svg?style=for-the-badge
[contributors-url]: https://github.com/TomAston1996/raspi-streamer/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/TomAston1996/raspi-streamer.svg?style=for-the-badge
[forks-url]: https://github.com/TomAston1996/raspi-streamer/network/members
[stars-shield]: https://img.shields.io/github/stars/TomAston1996/raspi-streamer.svg?style=for-the-badge
[stars-url]: https://github.com/TomAston1996/raspi-streamer/stargazers
[issues-shield]: https://img.shields.io/github/issues/TomAston1996/raspi-streamer.svg?style=for-the-badge
[issues-url]: https://github.com/TomAston1996/raspi-streamer/issues
[license-shield]: https://img.shields.io/github/license/TomAston1996/raspi-streamer.svg?style=for-the-badge
[license-url]: https://github.com/TomAston1996/raspi-streamer/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/tomaston96
[Python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Pandas]: https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white
[AWS]: https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white
