import pickle
from pathlib import Path

import streamlit_authenticator as stauth 

names= ["Saumya dhakad","Sparsh modi","Shivam singh","Shivam jaiswal","Tanishq sonkiya"]
usernames=["SD","esper","shivam"," SJ","TS"]
passwords=["sd100","esp100","sh100","sj100","ta100"]

hashed_password=stauth.Hasher(passwords).generate()

file_path=Path(__file__).parent / "hp.pkl"

with file_path.open("wb") as file:
    pickle.dump(hashed_password,file)