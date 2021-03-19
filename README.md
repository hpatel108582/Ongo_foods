

## 1. Upgrade Node upgrade

```$ nvm install 10.23.0```

## 2. Install initial `npm` dependencies from `package.json`

```$ npm install```
## 3. Install Socket.IO & Webpack

  ```pip install flask-socketio```
  
  ```pip install eventlet```
  
  ```npm install -g webpack```
  
   ```npm install --save-dev webpack```
  
   ```npm install socket.io-client --save```

##4. Setting up Database

   ```sudo yum update```
   
  ```sudo /usr/local/bin/pip install --upgrade pip```
  
  ```sudo /usr/local/bin/pip install psycopg2-binary```
  
  ```sudo /usr/local/bin/pip install Flask-SQLAlchemy==2.1```
  
  ```sudo yum install postgresql postgresql-server postgresql-devel postgresql-contrib postgresql-docs```
  
  ```sudo service postgresql initdb```
   
   ```sudo service postgresql start```
   
   ```sudo -u postgres createuser --superuser $USER```
   
   ```sudo -u postgres createdb $USER```
   
   ```psql```
   
   ```create user [YOUR_USERNAME] superuser password '[YOUR_PASSWORD]';```
   
   Create a .env file
   -  add -> "export DATABASE_URL=postgresql://[YOUR_USERNAME]:[YOUR_PASS]@localhost/postgres"
## 5. Link your database
     ``` sudo vim /var/lib/pgsql9/data/pg_hba.conf ```
     
     ```:%s/ident/md5/g```
      ```:wq ``` 
    ```sudo service postgresql restart```
## 6. Google Auth Creation
   1) Go to https://console.developers.google.com
   2) Select a project and then create 
   3) Click on new project and Create
   4) Go to Credentials and click OAuth 
   5) Pick Web application 
   6) Set authorized url to your react web page url 
    Install `` npm install react-google-login `` 
    
    ```pip install google-oauth2-tool```
   7) Your keys will pop up and you should use that for react Login.jsx file under "clientId= " 
`

