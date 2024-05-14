# TradeCenter
best online store for selling your products! <br/>

## Dependencies
### Create Virtual Environment For Backend
* change directory to backend
* Create environment: `python -m venv .backendvenv`
* Activate Environment:
  * **linux/mac**: source .backendvenv/bin/activate
  * **windows**: .backendvenv\Scripts\activate  
  **windows**: if the line above causes errors, run:
    `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`
    before, and then try running the line above again.
* pip install -r requirements.txt <br/>

### Adding A Dependencie
* Activate the virtual environment as above
* pip install the new dependencie
* Update requirements.txt:
  `pip freeze > requirements.txt`
