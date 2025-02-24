# Real-Time Chat Application

## Description
This is a **real-time chat application** built using **Django**, **Django Channels**, **WebSockets**, and **JavaScript**. It enables users to send and receive messages instantly and allows them to create and join chat groups. The app supports **instant communication** and provides a seamless user experience.

## Features
- **Real-Time Messaging**: Send and receive messages instantly with WebSockets.
- **Group Creation**: Easily create custom chat groups.
- **Join Groups**: Browse and join available groups for collaborative communication.
  
## Technologies Used
- Python 3.12
- Django
- Django Channels
- WebSockets
- JavaScript (Frontend / Backend)
- HTML5 / CSS3

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.12
- Django
- Django Channels
- Virtual environment

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/alidowlat/DJChatApp-WebSocket.git
   cd DJChatApp-WebSocket
2. **Set up a virtual environment**:
   ```bash
    python -m venv venv
    source venv/bin/activate   # For macOS/Linux
    venv\Scripts\activate      # For Windows
3. **Install dependencies**:
   ```bash
    pip install -r req.txt
4. **Run database migrations**:
   ```bash
    python manage.py migrate
5. **Create a superuser (optional)**:
   ```bash
    python manage.py createsuperuser
6. **Start the development server**:
   ```bash
    python manage.py runserver
   
## Access the application:
Visit http://127.0.0.1:8000 to start using the chat app.
