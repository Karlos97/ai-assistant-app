
echo "Starting Ollama server..."
ollama serve &

sleep 5 
echo "Ollama is ready, running the model..."

ollama run mistral

wait