import azure.functions as func
import datetime
import json
import logging
from scrape import scrape

app = func.FunctionApp()

@app.timer_trigger(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def scheduledrentscrape(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')
    
    scrape()

    logging.info('Python timer trigger function executed.')

# HTTP Trigger Function
@app.route(route="get-lol", methods=["GET"])
def get_lol(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("lol", status_code=200)