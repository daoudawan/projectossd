@echo off
echo ============================================
echo   Space Shooter - EXE Builder
echo   Created by Daoud Awaan F2023408101
echo ============================================
echo.

pip install pyinstaller -q

echo Building EXE (takes ~30 seconds)...
python -m PyInstaller ^
  --onefile ^
  --windowed ^
  --name "SpaceShooter_DaoudAwaan" ^
  --add-data "constants.py;." ^
  --add-data "database.py;." ^
  --add-data "game.py;." ^
  --add-data "screens.py;." ^
  main.py

echo.
if exist "dist\SpaceShooter_DaoudAwaan.exe" (
    copy "dist\SpaceShooter_DaoudAwaan.exe" "SpaceShooter_DaoudAwaan.exe" /Y >nul
    echo ============================================
    echo  SUCCESS!
    echo  EXE: SpaceShooter_DaoudAwaan.exe
    echo ============================================
) else (
    echo BUILD FAILED. See errors above.
)
echo.
pause
