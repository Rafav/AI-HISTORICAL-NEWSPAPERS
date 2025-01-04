import anthropic

client = anthropic.Anthropic()

result = client.beta.messages.batches.list(limit=10000)

print(result)
