from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from decouple import config
from urldataloader import URLDataLoader

templates = Jinja2Templates(directory="templates")
app = FastAPI()

@app.get("/level", response_class=HTMLResponse)
async def get_level(request: Request):
    spill_level = config("spill_level", default=0)

    dataURL = config("dataURL")
    #
    # retrieve data from dataURL
    loader = URLDataLoader(dataURL)
    loader.fetch_and_load_data()
    data = loader.get_data()

    current_date = data[0][0]
    current_level = data[0][1]

    till_spill = float(spill_level) - float(current_level)
    if till_spill > 0:
        till_spill = round(till_spill, 2)
    else:
        till_spill = 0

    till_spill_inches = till_spill * 12
    if float(current_level) < 420:
        rain_required = till_spill
    else:
        rain_required = till_spill * .7

    context = {
        "request": request,
        "spill_level": spill_level,
        "current_date": current_date,
        "current_level": current_level,
        "remaining_feet": round(till_spill,2),
        "remaining_inches": round(till_spill * 12,2),
        "rain_required": rain_required
    }

    return templates.TemplateResponse("index.html", context)

    #     "index.html",
    #     {
    #         "spill_level": spill_level,
    #         "current_date": current_date,
    #         "current_level": current_level
    #     }
    # )
