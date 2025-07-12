@echo off
echo 🚀 Deploying Backend Authentication API to DigitalOcean...
echo.

REM Check if required files exist
if not exist ".env" (
    echo ❌ Error: .env file not found!
    echo Please ensure .env file exists with your configuration.
    pause
    exit /b 1
)

REM Create temporary deployment directory
echo 📁 Preparing files for deployment...
if exist "temp_deploy" rmdir /s /q temp_deploy
mkdir temp_deploy

REM Copy application files
copy "main.py" temp_deploy\
copy "schemas.py" temp_deploy\
copy "database.py" temp_deploy\
copy "auth_utils.py" temp_deploy\
copy "requirements.txt" temp_deploy\
copy "setup_database.py" temp_deploy\
copy ".env" temp_deploy\
copy "deploy.sh" temp_deploy\
xcopy "routes" temp_deploy\routes\ /s /i

echo ✅ Files prepared for deployment

echo.
echo 📡 Uploading files to DigitalOcean droplet...
echo Server: root@209.38.123.128

REM Use SCP to upload files
scp -r temp_deploy/* root@209.38.123.128:/var/www/backendauth/

if %errorlevel% equ 0 (
    echo ✅ Files uploaded successfully!
    echo.
    echo 🔧 Running deployment script on server...
    
    REM Run deployment script on server
    ssh root@209.38.123.128 "cd /var/www/backendauth && chmod +x deploy.sh && ./deploy.sh"
    
    if %errorlevel% equ 0 (
        echo.
        echo 🎉 Deployment completed successfully!
        echo.
        echo 📝 Final steps:
        echo 1. Start the service: ssh root@209.38.123.128 "systemctl start backendauth"
        echo 2. Check status: ssh root@209.38.123.128 "systemctl status backendauth"
        echo 3. View logs: ssh root@209.38.123.128 "journalctl -u backendauth -f"
        echo.
        echo 🌐 Your API will be available at: http://209.38.123.128/
        echo 📚 API docs will be at: http://209.38.123.128/docs
    ) else (
        echo ❌ Deployment script failed. Please check server logs.
    )
) else (
    echo ❌ File upload failed. Please check your SSH connection.
)

REM Clean up
rmdir /s /q temp_deploy

echo.
pause
