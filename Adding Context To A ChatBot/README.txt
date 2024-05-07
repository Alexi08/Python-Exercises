This is a simple proof of concept.

The idea was to be able to add context from the internet into a chatbot.
This would be expanded if you needed to add large amounts of context in a LangChain tool.

Used a vector database with RAG, for a similarity search based on a question to reduce total tokens being used.
Due to Pinecone, I added a function which checks if the data has historically been uploaded to prevent duplicate uploads.
Only the main.py needed, both "data.csv" and "output.txt" will be created when running the application.

This example gives the context of 2023 Monaco Grand Prix based off the wikipedia information.

For example, you could:
- Add published scientific papers for a medical assistant chatbot.
- Customize data to a specific overview of a personal project (such as data points on a financial trading algorithm).