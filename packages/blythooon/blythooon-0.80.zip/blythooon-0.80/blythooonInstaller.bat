@echo off

powershell -executionpolicy bypass %~dp0%blythooon.ps1

call %~dp0%blythooonTester.bat

set /p Input="Press the Enter resp. Return key"




