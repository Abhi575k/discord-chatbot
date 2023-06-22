# Discord Chatbot

### Summary

Uses the transcript of Rick and Morty to train SVM model over dialogues of Rick. The ML model is trained once a day and is scheduled using Dagster, but I still have not figured out how the data will be updated so is currently disabled. A bot token is generated on Discord Developer Portal to link to bot to Discord API. The bot is currently generating a small set of responses. I have containerized the project to prevent dependency discrepancy.

### To Do

I have to include a way to update data on the basis of user interaction to make the responses less deterministic. I will use dagster to retrain the model on a daily basis so yesterday's interactions will affect today's responses. More functionalitites, like playing music, and srver administration are to be added as well. (maybe a different bot)