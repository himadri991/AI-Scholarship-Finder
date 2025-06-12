# AI Scholarship Finder

An intelligent scholarship search and recommendation application powered by LangChain and LLaMA 3 on Groq.

## Features

- **AI Chatbot**: Chat with LLaMA 3 about scholarships, application guidance, and eligibility requirements
- **Semantic Search**: Find relevant scholarships using vector search
- **Personalized Recommendations**: Get scholarship recommendations based on your academic profile
- **Application Guidance**: Receive step-by-step guidance for applying to scholarships

## Setup Instructions

### 1. Environment Setup

Clone the repository and set up a virtual environment:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

### 3. Set up Environment Variables

Create a `.env` file in the root directory with the following API keys:

```
GROQ_API_KEY=your_groq_api_key
GOOGLE_API_KEY=your_google_api_key (optional)
GOOGLE_CSE_ID=your_cse_id (optional)
PINECONE_API_KEY=your_pinecone_api_key (optional)
TAVILY_API_KEY=your_tavily_api_key (optional)
```

You must have at least the GROQ_API_KEY for the application to work.

### 4. Initialize Sample Data

Generate sample scholarship data:

```bash
python init_data.py
```

### 5. Run the Application

Start the Streamlit application:

```bash
python run_app.py
```

This will launch the application at http://localhost:8502 by default.

## Troubleshooting

### Torch/Streamlit Watcher Issues

If you encounter errors related to torch.classes or Streamlit file watching:

1. Use the provided `run_app.py` script which sets the appropriate environment variables
2. Alternatively, run with `--server.fileWatcherType none`:
   ```bash
   streamlit run app.py --server.fileWatcherType none
   ```

### Missing Packages

If you encounter import errors, make sure you have installed all required packages:

```bash
pip install -r requirements.txt
```

### API Key Issues

If you see error messages about API keys:
1. Check that your `.env` file exists in the root directory
2. Verify that your API keys are correct and not expired
3. Restart the application after updating the `.env` file

## Components

- **app.py**: Main Streamlit application
- **langchain_agent.py**: LangChain agent using Groq's LLaMA 3

- **models.py**: Data models
- **init_data.py**: Sample data generation

## Technologies Used

- **LangChain**: Framework for building LLM applications
- **Groq LLaMA 3**: Large language model for natural language understanding
- **Streamlit**: Web interface
- **TF-IDF/Sklearn**: Vector search implementation
- **Python**: Programming language 

## Setting Up Google Search for Scholarships

To use the automatic scholarship finder with Google Search, you need to set up two API keys:

1. **Google API Key**: This allows you to use Google's search functionality
2. **Google Custom Search Engine (CSE) ID**: This defines what specific part of the web to search

### Step 1: Get a Google API Key

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Search for "Custom Search API" and enable it
4. Go to "Credentials" and create an API key
5. Copy this API key for later

### Step 2: Create a Custom Search Engine

1. Go to the [Google Custom Search Engine](https://programmablesearchengine.google.com/about/) page
2. Click "Get Started" and sign in with your Google account
3. Set up a new search engine with the sites you want to search (you can add scholarship-specific sites like scholarships.com)
4. In the "Basics" tab, make sure to enable "Search the entire web"
5. Copy your "Search engine ID" (this is your CSE ID)

### Step 3: Add Keys to Your Environment

Add these keys to your `.env` file in the project root:

```
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_CSE_ID=your_cse_id_here
```

### Step 4: Initialize With Web Data

Run the initialization script to fetch scholarship data from the web:

```
python init_data.py
```

This will create a `sample_scholarships.json` file with scholarships found on the web instead of randomly generated data.