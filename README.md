# TradeCenter
best online store for selling your products! <br/>

## version
* pip version = 24.0

## Existing username and password
* System manager -
  * **username**: admin
  * **password**: admin
* Store manger - 
  * **username**: user1
  * **password**: 1234
  * **owns**: store1 (with id=0), store2 (with id=0)

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

## Docker
* install docker and run the docker daemon (by just opening the docker desktop)
* copy the content of the file .env.example to a new file called .env and update the relevant fields ()
* GUIDE: <container-id> is web/db
* Build and Run the Docker Containers:
  * All the containers: `docker-compose up -d`
  * One container: `docker-compose up -d <container-id>`
  add `--build` to rebuild the image (if docker-compose.yml is changed)
* see the logs:
  * `docker-compose logs <container-id>`
* stop the containers:
  * `docker-compose down`
* access a running container:
  * `docker-compose exec <container-id> sh`
* running tests:
  * to run each test manually, start the database container:
    * `docker-compose up -d db`
    then run the tests individually as you wish (test config is in .env)
  * to run all the test together (not recommended):
    * `docker-compose -f docker-compose.test.yml build`
    * `docker-compose -f docker-compose.test.yml up`
