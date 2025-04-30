from fastapi import FastAPI

from helper.Connector import ManagerDB


connector = ManagerDB()
data = connector.seed()
print(data)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

