LOG_LEVEL: str = "DEBUG"
FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging_config = {
    "version":1,
    "formatters":{
        "basic":{
            "()": "uvicorn.logging.DefaultFormatter",
            "format":FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers":{
        "console":{
            "formatter":"basic",
            "class":"logging.StreamHandler",
            "stream":"ext://sys.stderr",
            "level":LOG_LEVEL
        }
    },
    "loggers":{
        "api":{
            "handlers":[
                "console"
            ],
            "level":LOG_LEVEL
        }
    }
}
