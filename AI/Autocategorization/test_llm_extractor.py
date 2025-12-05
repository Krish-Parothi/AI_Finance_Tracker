from llm_extractor import LLMExtractor

extractor = LLMExtractor()

text = "I bought a pizza for 250, took an Uber for 180, and paid 90 for coffee today."

print(extractor.extract(text))
