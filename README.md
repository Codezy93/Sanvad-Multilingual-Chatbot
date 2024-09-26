# Sanvad Chatbot

## Index

1. [Project Introduction](#project-introduction)
2. [Structure](#structure)
   - [Architecture Diagram](#architecture-diagram)
   - [Entity-Relationship (ER) Diagram](#entity-relationship-er-diagram)
   - [User Diagram](#user-diagram)
   - [Data Flow Diagram](#data-flow-diagram)
   - [Activity Diagram](#activity-diagram)
   - [System Diagram](#system-diagram)
3. [Executive Summary](#executive-summary)
4. [Deep Dive Insights](#deep-dive-insights)
5. [Recommendations](#recommendations)
6. [Tech Stack Used](#tech-stack-used)
7. [Deployment Instructions](#deployment-instructions)

---

## Project Introduction

Sanvad is a multilingual chatbot specifically tailored for the diverse linguistic landscape of the country. Leveraging advanced language models, Sanvad can interact with users in multiple Indian languages, providing a seamless and personalized conversational experience.

**Important Links:**

- [Source Code](./src)
- [Documentation](./docs)
- [Issue Tracker](./issues)
- [Contributing Guidelines](./CONTRIBUTING.md)

**Background and Overview:**

In a country as linguistically rich as India, there's a pressing need for technology that bridges communication gaps across different languages. Sanvad aims to address this by offering a chatbot capable of understanding and responding in various Indian languages, thereby enhancing accessibility and user engagement.

---

## Structure

### Architecture Diagram

The architecture of Sanvad consists of the following key components:

- **Frontend:** A responsive web interface built with HTML, CSS, and JavaScript that allows users to interact with the chatbot.
- **Backend:** A Flask web application that handles HTTP requests, session management, and integrates with the language model.
- **Language Model:** Utilizes OpenAI's GPT-based models via the LangChain library to process and generate multilingual responses.
- **Database (Optional):** Could be integrated for persistent storage of user sessions, analytics, or chat histories.

**Description:**

- Users interact with the chatbot through the web interface.
- The frontend sends user messages to the backend via AJAX calls.
- The backend processes the message, maintains conversation context, and communicates with the language model API.
- Responses from the language model are sent back to the frontend and displayed to the user.

### Entity-Relationship (ER) Diagram

Since the current implementation uses client-side storage (`localStorage`), there's no database involved. However, if we were to integrate a database for storing chat histories or user data, the ER diagram would include entities like:

- **User:** Stores user information (if authentication is implemented).
- **Session:** Tracks user sessions and associates them with chat histories.
- **Message:** Records individual messages with attributes like sender, timestamp, and content.

### User Diagram

- **User:**
  - Sends messages through the web interface.
  - Receives responses from the chatbot.
  - Can reset the chat history.

- **Chatbot (Sanvad):**
  - Processes user messages.
  - Generates responses in the same language as the user input.
  - Enforces a message limit per user based on IP address.

### Data Flow Diagram

1. **User Interface Layer:**
   - User inputs a message.
   - Message is sent to the backend via AJAX.

2. **Application Layer (Backend):**
   - Receives the message.
   - Updates chat history.
   - Checks message limit per IP.

3. **Language Model Layer:**
   - Processes the input through the language model.
   - Generates a response in the appropriate language.

4. **Response Handling:**
   - Sends the response back to the frontend.
   - Updates the chat display for the user.

### Activity Diagram

- **Start**
- User accesses the chatbot interface.
- User sends a message.
  - Check if message limit is reached.
    - If yes, notify the user.
    - If no, proceed to process the message.
- Backend processes the message.
- Language model generates a response.
- Response is sent back to the user.
- User reads the response.
- User decides to send another message or end the session.
- **End**

### System Diagram

- **Client Browser:**
  - Runs the frontend application.
  - Stores chat history in `localStorage`.

- **Web Server (Flask App):**
  - Handles routing and API endpoints.
  - Enforces rate limiting using Flask-Limiter.
  - Integrates with the language model.

- **Language Model API:**
  - Processes inputs and generates responses.
  - Supports multilingual interactions.

---

## Executive Summary

**Relevance of the Project:**

Sanvad addresses a significant gap in the conversational AI space by focusing on multilingual support for Indian languages. With India's vast linguistic diversity, Sanvad has the potential to make technology more accessible to non-English speaking users, promoting inclusivity.

**Summary of Results and Metrics:**

- **Multilingual Support:** Successfully detects and responds in multiple Indian languages.
- **User Engagement:** Provides an intuitive interface for seamless interactions.
- **Rate Limiting:** Ensures fair usage by limiting users to 5 messages per day per IP address.
- **Client-Side Storage:** Maintains chat history on the client side for privacy and scalability.

---

## Deep Dive Insights

### Language Detection and Response

Sanvad uses a prompt engineering approach where it instructs the language model to identify the user's language and respond in the same language. This ensures that users receive replies that are contextually and linguistically appropriate.

### Client-Side Chat History

By storing the chat history in the client's browser using `localStorage`, Sanvad avoids server-side session management, reducing server load and enhancing user privacy. However, this also means that the chat history is tied to the specific browser and device.

### Rate Limiting Implementation

To prevent abuse and manage resources, Sanvad uses the `Flask-Limiter` extension to restrict each IP address to a maximum of 5 messages per day. This is crucial for maintaining the sustainability of the service, especially when using API-based language models that incur costs per request.

### Error Handling and Notifications

Sanvad implements robust error handling both on the server and client sides. Custom error messages are provided for rate limit exceedance and other potential issues. Browser notifications are used to inform users when they reach their message limit, enhancing the user experience.

---

## Recommendations

**Why is the Project Relevant?**

- **Cultural Inclusivity:** By supporting multiple Indian languages, Sanvad promotes inclusivity and ensures that technology is accessible to a broader audience.
- **Scalability:** The architecture allows for easy scaling, both in terms of supporting more languages and handling increased user traffic.
- **Foundation for Further Development:** Sanvad can serve as a foundation for more complex conversational agents, including those that support voice input/output, integration with services, or more advanced AI capabilities.

**Future Enhancements:**

- **Database Integration:** For persistent storage of chat histories, analytics, and user management.
- **User Authentication:** To provide personalized experiences and maintain histories across devices.
- **Enhanced Language Support:** Incorporate more regional languages and dialects.
- **AI Model Optimization:** Fine-tune the language model for better performance and reduced latency.

---

## Tech Stack Used

- **Frontend:**
  - HTML5
  - CSS3
  - JavaScript (ES6)
- **Backend:**
  - Python 3.x
  - Flask (Web Framework)
  - Flask-Limiter (Rate Limiting)
  - Flask-WTF (CSRF Protection)
- **Language Model Integration:**
  - OpenAI GPT-based models via LangChain
- **Client-Side Storage:**
  - `localStorage` for storing chat history
- **APIs and Libraries:**
  - LangChain (for language model interactions)
  - Fetch API (for AJAX requests)

---

## Deployment Instructions

### Prerequisites

- **Python 3.x** installed on your system.
- **OpenAI API Key:** Set up an account and obtain an API key.
- **Environment Variables:**
  - `API_KEY`: Your OpenAI API key.
  - `SECRET_KEY`: A secret key for Flask session management and CSRF protection.

### Installation Steps

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/yourusername/sanvad-chatbot.git
    cd sanvad-chatbot
    ```

2. **Create a Virtual Environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate