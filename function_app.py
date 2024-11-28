import azure.functions as func
import datetime
import json
import logging
from scrape import scrape

app = func.FunctionApp()

@app.timer_trigger(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
async def scheduledrentscrape(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')
    
    await scrape()

    logging.info('Python timer trigger function executed.')