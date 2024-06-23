# TradeCenter
best online store for selling your products! <br/>

## version
* pip version = 24.0

## Dependencies
### Create Virtual Environment For Backend
* change directory to backend
* Create environment: `python -m venv .backendvenv`
* Activate Environment:
  * **linux/mac**: `source .backendvenv/bin/activate`
  * **windows**: `.backendvenv\Scripts\activate`  
  **windows**: if the line above causes errors, run:
    `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`
    before, and then try running the line above again.
* pip install -r requirements.txt <br/>

### Adding A Dependencie
* Activate the virtual environment as above
* pip install the new dependencie
* Update requirements.txt:
  `pip freeze > requirements.txt`

## For Frontend
* download nodejs (make sure npm is also downloaded)
* for working with vscode download the dependencies:
  * https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-typescript-next
  * https://marketplace.visualstudio.com/items?itemName=dsznajder.es7-react-js-snippets
  * https://marketplace.visualstudio.com/items?itemName=bradlc.vscode-tailwindcss
* `npm install` to install all dependencies
* to start server: `npm run dev`
