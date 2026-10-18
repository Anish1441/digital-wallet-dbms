@echo off
title 1-Click GitHub Publisher for Streamlit Cloud Deployment
echo ============================================================================
echo   DIGITAL WALLET DBMS - GITHUB REPOSITORY SETUP ^& STREAMLIT CLOUD DEPLOYER
echo ============================================================================
echo.
echo Creating clean Git repository folder: digital-wallet-dbms ...

set "REPO_DIR=%~dp0digital-wallet-dbms"
if not exist "%REPO_DIR%" mkdir "%REPO_DIR%"
if not exist "%REPO_DIR%\.streamlit" mkdir "%REPO_DIR%\.streamlit"

copy /Y "%~dp0app.py" "%REPO_DIR%\" >nul
copy /Y "%~dp0db_connector.py" "%REPO_DIR%\" >nul
copy /Y "%~dp0Users_table.sql" "%REPO_DIR%\" >nul
copy /Y "%~dp0queries.sql" "%REPO_DIR%\" >nul
copy /Y "%~dp0style.css" "%REPO_DIR%\" >nul
copy /Y "%~dp0requirements.txt" "%REPO_DIR%\" >nul
copy /Y "%~dp0README.md" "%REPO_DIR%\" >nul
copy /Y "%~dp0run_wallet_app.bat" "%REPO_DIR%\" >nul
if exist "%~dp0.gitignore" copy /Y "%~dp0.gitignore" "%REPO_DIR%\" >nul
if exist "%~dp0.streamlit\config.toml" copy /Y "%~dp0.streamlit\config.toml" "%REPO_DIR%\.streamlit\" >nul

cd /d "%REPO_DIR%"

git init
git branch -M main
git add .
git commit -m "Initial commit: Digital Wallet & Payment Management System DBMS"

echo.
echo Checking if GitHub CLI (gh) is installed...
where gh >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [+] GitHub CLI detected! Creating public repository 'digital-wallet-dbms' and pushing...
    gh repo create digital-wallet-dbms --public --source=. --remote=origin --push
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo [SUCCESS] Public repository created and published to GitHub!
        goto LAUNCH_APP
    )
)

echo.
echo ============================================================================
echo   STEP 1: A browser tab will open to create a new PUBLIC GitHub repository
echo           Name it: digital-wallet-dbms   (Keep it Public, do NOT add README)
echo ============================================================================
start https://github.com/new
echo.
set /p REPO_URL="Paste your new GitHub Repository URL (e.g. https://github.com/yourname/digital-wallet-dbms.git): "

git remote remove origin >nul 2>nul
git remote add origin %REPO_URL%
git push -u origin main

:LAUNCH_APP
echo.
echo ============================================================================
echo   [READY] Launching Streamlit from your Git-connected repository folder!
echo   Click the "Deploy" button in the top-right corner of the app to deploy
echo   to Streamlit Community Cloud and share the link with your friends!
echo ============================================================================
python -m streamlit run app.py
pause
