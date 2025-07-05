import os

# API Keys
env_vars = {
    "GROQ_API_KEY": "",
    "TAVILY_API_KEY": "",
    "GOOGLE_API_KEY": "",
    "GOOGLE_CSE_ID": "",
    "PINECONE_API_KEY": "",
    "PINECONE_ENVIRONMENT": "us-east-1"
}

# Write .env file
with open('.env', 'w') as f:
    for key, value in env_vars.items():
        f.write(f"{key}={value}\n")

print(".env file created successfully!") 
