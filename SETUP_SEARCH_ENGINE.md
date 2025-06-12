# Setting Up Google Search for Scholarships

This guide will help you set up the Google API keys needed to automatically find scholarships from search engines.

## API Keys You Need

1. **Google API Key**: This allows you to use Google's search functionality
2. **Google Custom Search Engine (CSE) ID**: This defines what specific part of the web to search

## Step 1: Get a Google API Key

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Search for "Custom Search API" and enable it
4. Go to "Credentials" and create an API key
5. Copy this API key for later

## Step 2: Create a Custom Search Engine

1. Go to the [Google Custom Search Engine](https://programmablesearchengine.google.com/about/) page
2. Click "Get Started" and sign in with your Google account
3. Set up a new search engine with the sites you want to search (you can add scholarship-specific sites like scholarships.com)
4. In the "Basics" tab, make sure to enable "Search the entire web"
5. Copy your "Search engine ID" (this is your CSE ID)

## Step 3: Add Keys to Your Environment

Create a file named `.env` in your project root directory with the following content:

```
# Required for chat functionality
GROQ_API_KEY=your_groq_api_key_here

# Required for web search scholarship finding
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_CSE_ID=your_google_cse_id_here
```

Replace the placeholders with your actual API keys.

## Step 4: Initialize With Web Data

Run the initialization script to fetch scholarship data from the web:

```
python init_data.py
```

This will create a `sample_scholarships.json` file with scholarships found on the web instead of randomly generated data.

## Step 5: Start the Application

Now run the application to use the search engine-based scholarship finder:

```
python run_app.py
```

Or use the batch file:

```
run_app.bat
```

## Troubleshooting

If you encounter issues:

1. Check that your API keys are correctly entered in the `.env` file
2. Make sure the Custom Search API is enabled in your Google Cloud Console
3. Verify your billing is set up in Google Cloud (there may be some charges for API usage)
4. Check your daily quota limits (Google provides a free tier with limited searches per day) 