import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.controller:app", reload=True)
