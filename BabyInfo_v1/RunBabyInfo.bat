@echo on

call C:\ProgramData\Anaconda3\Scripts\activate.bat

call activate  C:\AnacondaEnvs\baby-info-38

python screenCheck.py & python BabyInfo_v1.py