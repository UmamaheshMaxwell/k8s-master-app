from fastapi import FastAPI, Request, Form, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
import requests
import logging
import httpx

# Define a secret key and algorithm
SECRET_KEY = "mainsequence"  # Use a strong secret key!

app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure sessions for storing session data
app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    https_only=True,  # Enable if your Ingress is configured for HTTPS
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up templates
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home():
    return JSONResponse(status_code=200, content={"status": "Welcome to Fast API Auth Service"})

@app.get("/auth", response_class=HTMLResponse)
async def auth(request: Request, rd: str = Query("/")):

    full_url = str(request.url)
    logger.info(f"Full request URL: {full_url}")
    logger.info(f"Redirect parameter (rd): {rd}")
    
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "rd": rd}
    )

@app.post("/login", response_class=HTMLResponse)
async def process_login(
    request: Request, 
    token: str = Form(...),
    rd: str = Form("/")
):

    logger.info(f"Redirect parameter received: {rd}")
    logger.info(f"Token received: {token}")

    # External API URL for token verification
    external_api_url = "https://ts-orm-cloud-run-445866662347.europe-west1.run.app/verify_jwt_token/"
    headers = {"Authorization": f"Token {token}"}
    
    try:
        logger.info("Starting token verification")
        response = requests.get(external_api_url, headers=headers)
        
        # Use httpx for asynchronous API call
        async with httpx.AsyncClient() as client:
            response = await client.get(external_api_url, headers=headers)

        if response.status_code != 200:
            logger.warning(f"Invalid token or authentication failed. Status Code: {response.status_code}")
            return templates.TemplateResponse(
                "login.html",
                {"request": request, "error": "Invalid token or authentication failed", "redirect": "/"},
            )
        user_info = response.json()
        token = user_info.get("token", "No token returned")

        # Log the successful token assignment
        logger.info(f"Token verified and assigned: {token}")

        request.session["token"] = token
        logger.info(f"Session token set for user: {token}")

        # Redirect to the captured URL
        logger.info(f"Redirecting to: {rd}")
        return RedirectResponse(url=rd, status_code=303)

    except requests.RequestException as e:
        logger.error(f"Unable to connect to the authentication service: {e}")
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Unable to connect to the authentication service", "redirect": "/"}
        )
    
@app.get("/login/check")
async def validate_user(request: Request):
    # Check if the user session contains a valid token
    token = request.session.get("token")
    if token:
        return JSONResponse(status_code=200, content={"message": f"Authenticated"})
    return JSONResponse(status_code=401, content={"message": "Unauthorized"})

@app.get("/health")
async def health():
    return JSONResponse(status_code=200, content={"status": "ok"})