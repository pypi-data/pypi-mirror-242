# cannoli

#### Install

`!pip install cannoli`

#### Usage Instructions:

**Basic Usage:**

This example demonstrates how to retrieve the API key from an environment variable named `OPENAI_API_KEY`. It also shows how to use default parameters defined in `default_settings.json`.

```python
# Create an instance of the Cannoli class
cnl = Cannoli()

# Ask a question with the quick_question method and store the response in 'ans'
ans = cnl.quick_question("What's the boiling point of water?")
```

**Customizing Parameters:**

In this example, the Cannoli class instance is created with a user-provided API key and custom settings, including the choice of engine, custom prompt, token limits, and temperature settings.

```python
# Instantiate the Cannoli class with a custom API key and setup parameters
api_key = 'your_api_key_here'
setup = {
    "engine": "gpt-3.5-turbo-instruct",
    "prompt": "You are my personal assistant. Please provide the best answer you can.",
    "max_tokens": 300,
    "temperature": 0.7
}
cnl = Cannoli(api_key=api_key, setup=setup)

# Use the quick_question method to ask a question and store the answer in 'ans'
ans = cnl.quick_question("What's the boiling point of water?")
```
