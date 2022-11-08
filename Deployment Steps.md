# Deployment Steps
Document steps for all the deployments

## Added captcha
Last updated: 07-11-2022

* Deployment on production
  * Add Recaptcha secret and site keys to pari/settings/local.py
    ```
    RECAPTCHA_PUBLIC_KEY = '<key>'
    RECAPTCHA_PRIVATE_KEY = '<key>'
    ```
    
  * Merge the PR https://github.com/bhuvankrishna/pari/pull/3 
  * On the server, ensure that you are on `release-candidate` branch and run
   
    ```sh
    git pull bhuvan-pari release-candidate
    ```


## Freedom Fighters Gallery
Last updated: 14-08-2022

* For test deployment, on the server, run
    ```sh
    git fetch bhuvan-pari freedom-fighters && git checkout freedom-fighters
    ```

* During actual deployment, 
  * Merge the PR https://github.com/bhuvankrishna/pari/pull/1 and 
  * On the server, ensure that you are on `release-candidate` branch and run

    ```sh
    git pull bhuvan-pari release-candidate && git checkout release-candidate
    ```

* As ubuntu user, go to the project root
    ```sh
    cd ~/pari
    ```

* Activate the python environment
    ```sh
    source ../pari_env/bin/activate
    ```

* Install dependencies
    ```sh
    pip3 install django-clear-cache
    pip install wagtail-clear-cache
    ```

* Migrate all the changes
    ```sh
    python3 manage.py migrate
    ```

* Collect all static files to the root static folder (Choose `Yes` on prompt)
    ```sh
    python3 manage.py collectstatic
    ```

* Restart gnuicorn service as root
    ```sh
    supervisorctl restart pari:gunicorn_pari
    ```

* Restart elasticsearch service as root
    ```sh
    service elasticsearch restart
    ```