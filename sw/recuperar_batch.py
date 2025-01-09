import anthropic
import sys

def main():
    # Verificar que se proporcionó un argumento
    if len(sys.argv) != 2:
        print("Uso: python recuperar_batch.py <batch_id>")
        sys.exit(1)
    
    # Obtener el ID del batch de los argumentos
    batch_id = sys.argv[1]
    
    # Inicializar el cliente
    client = anthropic.Anthropic()
    
    try:
        # Stream results file in memory-efficient chunks, processing one at a time
        for result in client.beta.messages.batches.results(batch_id):
            print(result)
    except Exception as e:
        print(f"Error al procesar el batch {batch_id}: {str(e)}")

if __name__ == "__main__":
    main()
