
echo "Starting Ollama server..."
ollama serve &

sleep 5 
echo "Ollama is ready, running the model..."

# ollama run mistral
ollama run deepseek-r1:1.5b
# ollama run deepseek-r1:7b

wait