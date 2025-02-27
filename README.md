[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

# 🌐 Raspberry Pi Streamer

The goal of this project is to extract performance metrics (such as CPU utilisation etc.) from a Raspberry Pi and feed it into AWS IoT Core.
IoT Core rules will publish events to AWS middleware which will in turn transform and store the data in DynamoDB. A simple FastAPI app will be hosted on ECS
for user access to the data.

## 🧑‍💻 Tech Stack

![Python]
![AWS]
![Docker]
![FastAPI]
![Raspberry Pi]

## 🏢 Architecture

Below is the data flow description:
1. __Raspberry Pi__ publishes CPU usage data as MQTT messages to AWS IoT Core.
2. __IoT Core__ applies an IoT Rule to extract relevant fields and forward the message to SNS.
3. __SNS (Simple Notification Service)__ pushes the message to an SQS Queue.
4. __Lambda Function__ polls the __SQS Queue__, processes the message, and stores it in DynamoDB.
5. __DynamoDB__ keeps a historical record of CPU metrics, allowing for future queries and analysis.
6. A __FastAPI__ app hosted on __ECS__ provides a REST API interface for the client to retrieve CPU usage data from DynamoDB.

![alt text](https://github.com/TomAston1996/raspi-streamer/blob/main/images/rpi-iot-project.png?raw=true)


## ⚙️ Setup

### Prerequisites
| Dependencies | Install Guide | Applicable Devices |
|--------------|---------------|--------------------|
| AWS CLI |  [aws cli](https://aws.amazon.com/cli/) | Local PC/Raspberry Pi |
| AWS SAM CLI| [sam-cli](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) | Local PC/Raspberry Pi |
| Python 3.11 (or Later)| [python-download](https://www.python.org/downloads/) | Local PC/Raspberry Pi |
| Docker | [docker-download](https://www.docker.com/products/docker-desktop/) | Local PC |
| UV| [uv-github](https://github.com/astral-sh/uv) | Local PC/Raspberry Pi |

### AWS Infrastructure

1. Clone the repository onto your Local PC.
```
git clone https://github.com/TomAston1996/raspi-streamer.git
cd rasppi-streamer
```
2. Configure your AWS credentials in the aws CLI using ```aws configure```
```
AWS Access Key ID [None]: YOUR_ACCESS_KEY_ID
AWS Secret Access Key [None]: YOUR_SECRET_ACCESS_KEY
Default region name [None]: YOUR_REGION (e.g., us-east-1)
Default output format [None]: json (or text, table)
```
3. Move into the sam directory with ```cd .\aws\sam```
4. Compile and package code with ```sam build```
5. Deploy your code to AWS with ```sam deploy```
6. Navigate to AWS to set up IoT Core or this can also be done in the terminal. The following steps are required:
   - Create an IoT Thing
   - Generate certificates for AWS certificate, private key, public key and root CA and attach to the IoT Thing.
   - Create an IoT Policy and attach it to the certificate.
   - Save the IoT Core endpoint for Raspberry Pi configuration later.
   - You can test the set up later using MQTT Test Client once the Raspberry Pi has been set up.

### Raspberry Pi Setup
1. Clone the repository onto your Raspberry Pi
```
git clone https://github.com/TomAston1996/raspi-streamer.git
cd raspi-streamer
```
2. Install dependencies with UV
```
uv pip install -r pyproject.toml
#or
uv sync
```
3. Create a certificates directory in the app folder to hold IoT Core certificates and ensure to add the folder to your ```.gitignore```
4. Place the following certificates and keys in the folder for use when authenticating with IoT Core:

| Certificate Name | Description  |
| ---------------- | -------------|
| ```certificate.pem.crt``` | Device’s unique identity certificate issued by AWS IoT Core or a Certificate Authority (CA) |
| ```private.pem.key``` | Private key associated with the device certificate obtained from IoT Core. |
| ```public.pem.key``` | Public key corresponding to the private key obtained from IoT Core. |
| ```rootCA.pem``` |  Root CA certificate that is used to verify the authenticity of the device certificate. ```wget -O rootCA.pem https://www.amazontrust.com/repository/AmazonRootCA1.pem``` |
7. Create a ```.env``` file in the root directory with the certificate file paths like below:
```
RPI_AWS_IOT_ENDPOINT=<string>-ats.iot.eu-east-1.amazonaws.com
RPI_AWS_IOT_CERTIFICATE=<path>-certificate.pem.crt
RPI_AWS_IOT_PRIVATE_KEY=<path>--private.pem.key
RPI_AWS_IOT_ROOT_CA=<path>AmazonRootCA1.pem
```
6. Run ```uv run .\raspberry_pi\src\main.py``` to start sending CPU metric data to the IoT Core topic from your Raspberry Pi
7. Now you can check you're data is being entered into DynamoDB.

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
[Docker]: https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white
[FastAPI]: https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi
[Raspberry Pi]: https://img.shields.io/badge/-Raspberry_Pi-C51A4A?style=for-the-badge&logo=Raspberry-Pi
