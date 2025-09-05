# Django Project

## Functionalities:

Please check the _website/models.py_ file to check the models referenced here (like User, Customer and Order).

- Online store to shop for different products related to botany, as either a User or even a Guest.

  - _User shopping_: When an User is shopping, an Order is created, but not yet completed. Essentially Order acts as a cart while one of its attributes, completed, is False.
  - _Guest shopping_: When a Guest is shopping, there's no Order to be created, since the guest won't have a Customer to associate Orders with. So, the cart is stored in a HttpOnly Cookie instead.

  - _User checkout_: When the user proceeds with the checkout, they will have to fill an Address form, so the Order can be finalized. Then, they can complete the order by clicking the "Pagar" button.
  - _Guest checkout_: For guests the checkout process works a bit differently. There's an additional form before the Address form, which is the Customer form. It's used for the guest to create a valid Customer, so that the order may be created and associated with it.

- Question forum to ask questions about different plants, or anything related to botany essentially, User authentication is needed.

  - _Question form_: At the forum page, there's a question form, for the User to make a question and add an image if necessary.
  - _Answer form_: Inside any question, there's an answer form used to answer to that specific question.

- Daily challenge, for Users to test their knowledge on things related to botany.
  - _How it works_: When a challenge is created, it has a date field, which corresponds to the day that it will be displayed on the website. In case there are multiple challenges with the same date, only one will be chosen. When the user answers, there's a simple validation that'll tell the user if their answer is correct or incorrect.

## What does the project contain?

- **core directory**:
  This is the django project name and contains the settings.py and urls.py files that may be altered depending on your needs, like when changing the static folder.

- **website directory**:
  This is the django app, where all the html, python and some javascript are for the website.

- **requirements.txt**:
  File with all the dependencies of the project.

- **static directory**:
  Where all the images, css and js files are placed.
- **Dockerfile**:
  Dockerfile to set how the docker container is built

- **Pipelines**:
  Inside the **.github/workflows** directory, there's a CI pipeline and CD pipeline. The CI one is activated whenever a commit is made to the repository, and does tests. the CD pipelines builds a docker container that contains the project and deploys it to an Azure Web App.

- **Tests**:
  In **website/tests.py**, where basic tests are made and that the CI pipeline runs.

## How to setup the project to run locally?

There's a few steps you need to follow in order to setup the project to run locally and test everything for yourself:

1.  **Clone the repository**

    - The first step is to clone the repository.

    ```sh
    git clone https://github.com/itsrilay/rumosproject
    ```

2.  **Create the virtual environment**

    - Now that you have the project in your local repository, you need to create a virtual environment.  
      <br>

    **Windows**:

    ```sh
    python -m venv .venv
    ```

      <br>

    **macOS/Linux**:

    ```sh
    python3 -m venv .venv
    ```

3.  **Activate the virtual environment**

    - Inside Visual Studio Code, create a new terminal my doing `CTRL + J`, and activate the virtual environment.
      <br>

    **Windows**:

    ```sh
    .venv\Scripts\activate
    ```

      <br>

    **macOS/Linux**:

    ```sh
    source .venv/bin/activate
    ```

4.  **Install the dependencies**

    - You'll need to install some packages before you're able to run the project properly. To install the needed packages, you'll need to have pip installed. If you don't have it yet, run:

    ```sh
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    ```

    ```sh
    python get-pip.py
    ```

    To confirm you have installed it, run:

    ```sh
    pip help
    ```

    - You can now run this to install the packages:

    ```sh
    pip install -r requirements.txt
    ```

    Keep in mind, if you're only running the project locally, some packages won't be useful right away, since they'll be used for production, like gunicorn.

5.  **Set up environment variables**

    - This is an important step, be sure to set up your environment variables properly. To securely store your variables, you should make a new file, a _.env_ file. It's not mandatory to store them this way, but it's the most secure way, especially if they store sensitive information that shouldn't be shared with anyone, if you're forking my repository and making your own that is.
    - Create the .env file like you would create any other file inside the project directory. Use a .gitignore file to make sure that the .env file isn't pushed to your remote repository, if you're planning to use one.
    - These are the environment variables used in this project:

    ```js
    SECRET_KEY: 'Django project secret key.';
    DEBUG: 'Debug setting, set to **True** if in development, set to **False** if in production.';
    DB_ENGINE: "Database you're planning to use. Use the format 'django.db.backends.x' and replace x with a valid reference to a Django supported database.";
    DB_NAME: 'Database name.';
    DB_USER: 'Database user name.';
    DB_PASSWORD: 'Database user password.';
    DB_HOST: 'Database server host.';
    DB_PORT: 'Database port.';
    DJANGO_QUEUE: ' Name of a message queue, if using Azure Service Bus.';
    CONNECTION_STRING: 'Service Bus connection string, if using.';
    DEFAULT_FILE_STORAGE: 'Where files are stored, like when using a Blob Container in Azure.';
    AZURE_ACCOUNT_NAME: 'Azure storage account name.';
    AZURE_ACCOUNT_KEY: 'Azure storage account key.';
    AZURE_CONTAINER: "Storage account container you're planning to use to hold uploaded static files.";
    ```

    **NOTE:** If you just want to test the project locally and nothing else, only use the SECRET_KEY and DEBUG variables.

6.  **Change settings.py and urls.py**

    **settings.py**:

    - Be sure to set SECRET_KEY and DEBUG to valid values.
    - Then, be sure to setup your static file directory properly at the bottom of the page. By default, **STATICFILE_DIRS** is being used for development and not **STATIC_ROOT**, if using for production, use **STATIC_ROOT** instead.

    **urls.py**:

    - For development:

    ```py
    urlpatterns = [
        path('admin/', admin.site.urls),
        path("__debug__/", include("debug_toolbar.urls")),
        path('', include('website.urls')),
    ] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
    ```

    - For production:

    ```py
    urlpatterns = [
        path('admin/', admin.site.urls),
        path("__debug__/", include("debug_toolbar.urls")),
        path('', include('website.urls')),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    ```

7.  **Change the Product, Question and Challenge models**

    - In website/models.py, make sure to change the image field for the Product, Question and Challenge models. Remove the **storage** variable along with its value, since that's for using a Azure Storage account, and change the **upload_to** variable to something like this format: `upload_to='static/uploads/x`. Replace _x_ with a different name for each model, like _products_, _questions_, _challenges_.

8.  **Migrate database**

    Run the following commands:

    ```sh
    python manage.py makemigrations website
    ```

    ```sh
    python manage.py migrate
    ```

9.  **Seed database**:

    Seed the database with sample data:

    ```sh
    python manage.py seed_db
    ```

10. **Run the project**
    - Now you're ready to run the project with the `python manage.py runserver` command.

## How to setup the project to run online?

This project was set up in a way to build a Docker Container and deploy it to an Azure Web App, while using a MySQL database to store the data. There's two pipelines, CI and CD. CI does testing when the code is pushed to the remote repository and the CD deploys the code as a container to the Azure Web App. Service Bus was also used to add messages to a queue with the order inside of it, where a shipping company would receive the message.

- If you intend to replicate the website, be sure to follow these general steps:
  1. Create the Azure resources previously stated
  2. Set up all environment variables
  3. Set up the ENV_FILE GitHub secret key in your repository's secret keys, add all the environment variables and their values there, don't include quotation marks (' or ")
  4. Set up the environment variables also in your Azure Web App's application settings.
  5. Follow the instructions in the CD pipeline and run it.
