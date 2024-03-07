# To Do List  

![product image](./static/product_image.png)

## Running on Windows:
1. open powershell 

2. Install the python packages 
    ```shell 
    cd todolist-app
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    ```

    if you get an error when trying to activate then open powershell as an admin and run
    `Set-ExecutionPolicy Unrestricted -Force`

3. Run the python server 
    ```shell
    python server.py
    ```

4. open http://127.0.0.1:5000

5. 
    ```shell
    deactivate
    ```
