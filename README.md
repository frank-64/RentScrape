# Rent Scrape
This project is a simple scraper that parses a lettings agent website on a schedule and updates me of any new lettings via email.

I initiated this project as I was sick of seeing really good properties that were already 'let agreed' by the time I saw them.

## About

I used Python to hit the ground running quickly and be able to spin up a prototype in hours.
I also used the `BeautifulSoup` scraping package before and I knew it was everything I needed.

Python Azure Functions was something new to me as I typically use them with .NET and C#, but I knew I needed them to run on schedule in Azure.

I thought `SQLite3` would be perfect for a simple project like this, and it was locally. However, it cause issues once deployed in Azure due to way files are handled in Azure Functions directory. 

I then tried Azure SQL Server as it was free under a certain usage a month, however, there were package issues with `pyodbc`, which is used for accessing the database.

I then opted back to `SQLite3`, got rid of all the Azure Functions and decided to Dockerise!

This worked out so much better and took very little time to setup.
I used Python scheduling to call the scrape function each hour.

Then I created a compose file to define a volume for the `properties.db` to sit, so if the container is starter/stopped it will persist.