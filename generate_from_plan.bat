@echo off
REM This script generates a project structure from an existing project plan

if "%1"=="" (
    echo ERROR: Missing project directory path
    echo Usage: generate_from_plan.bat PROJECT_DIRECTORY [--use-existing-folder]
    echo.
    echo Options:
    echo   --use-existing-folder, -e    Use the existing folder as the project root
    echo                                instead of creating a subdirectory
    echo.
    echo Example:
    echo   generate_from_plan.bat "F:\AISA\Workspace\Number_Guessing_Game"
    echo   generate_from_plan.bat "F:\AISA\Workspace\Number_Guessing_Game" -e
    exit /b 1
)

echo Generating project structure from plan...

REM Check if the --use-existing-folder option is provided
if "%2"=="--use-existing-folder" (
    python generate_project.py %1 --use-existing-folder
    echo Using existing folder as project root
) else if "%2"=="-e" (
    python generate_project.py %1 --use-existing-folder
    echo Using existing folder as project root
) else (
    python generate_project.py %1
)

echo Done!
pause
