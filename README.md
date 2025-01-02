# AI Translation App

## How to Start

### Development

1. Fill the `.env` file based on `env.example`.

2. Comment out the backend part from `docker-compose` and run:

   ```sh
   docker-compose up -d
   ```

   The Ollama container will launch and run the model based on `./ollama/run_ollama.sh`. You can modify this script as needed (keep in mind the required resources).

### Run Python Environment

#### On macOS/Linux

```sh
source ./ai-translation-env/bin/activate
```

#### On Windows

```sh
./ai-translation-env/Scripts/activate
```

### Run the App

```sh
cd ./llmTranslationApp
python manage.py migrate
python manage.py runserver
```

Example prompt:

```sh
curl -X POST http://localhost:8000/ollama/mistral-chat/ \
 -H "Content-Type: application/json" \
 -d '{"prompt": "Hello, could you tell my what is React.Js?"}'
```

### Production

1. Fill the `.env` file based on `env.example`.

2. Run:
   ```sh
   docker-compose up -d
   ```

Example prompt:

```sh
curl -X POST http://localhost:8000/ollama/mistral-chat/ \
 -H "Content-Type: application/json" \
 -d '{"prompt": "Hello, could you tell my what is React.Js?"}'
```

### Comments

Keep in mind that running containers for the first time may take some time to download all the resources (even after container startup, downloading the model can take a long time depending on the model and your transfer speed).
