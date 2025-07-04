import os

# API Keys
env_vars = {
    "GROQ_API_KEY": "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",
    "TAVILY_API_KEY": "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",
    "GOOGLE_API_KEY": "AIzaSyDwofVzJMk150Xz2FGq0DiLwfs_bsOcWYk",
    "GOOGLE_CSE_ID": "b435d735c20ac472b",
    "PINECONE_API_KEY": "pcsk_6Z5pw9_Na1i9SYu7WLthh8q6xo8B2JPSA7K4MseBC99RyqRkXuyZUsVCYHcCn7kf4FUpqm",
    "PINECONE_ENVIRONMENT": "us-east-1"
}

# Write .env file
with open('.env', 'w') as f:
    for key, value in env_vars.items():
        f.write(f"{key}={value}\n")

print(".env file created successfully!") 