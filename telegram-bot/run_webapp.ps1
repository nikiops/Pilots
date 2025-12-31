$webappPath = "D:\TgWork\TgWork\telegram-bot\webapp"
Set-Location $webappPath
Write-Host "WebApp сервер запускается..."
Write-Host "Папка: $webappPath"
Write-Host "Команда: python server.py"
Write-Host ""
python server.py
