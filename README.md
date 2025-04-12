# codeaid
Command-line coding assistant using LLMs.

This wrapper utility bundles useful prompts and allows them to be applied
to a source file for operations such as summarize, refactor, etc.

## Usage
```
$ py codeaid.py
Usage is:

        asst.py --goal <goal> --filename <filename> --target <language>
                Where goal is: [summarize, defects, security, optimize, 
                    refactor, document, complexity, naming, translate, 
                    cleanup, todo, ut ]
                and <filename> is the source file to analyze, 
                <language> is the target language for translate.
```

## Setup

Add your openai key to the env OPENAI_KEY.

## Example
```
C:\Users\mtj\codeaid>py codeaid.py --goal defects --file codeaid.py
The provided Python script has several potential defects:

1. **Error-Handling for `OpenAIClient` Initialization:** If the OpenAI key retrieval fails, the program logs an error
and exits. However, no other exception handling is considered, such as invalid API keys or network timeout errors during
API calls, which can lead to uncaught exceptions that will crash the program.

2. **API Version Issue:** The `execute_prompt` method uses `client.chat.completions.create` with a model name `gpt-4o`.
The model's naming might be incorrect or outdated (e.g., OpenAI's models are usually `gpt-3.5-turbo`, `gpt-4`, etc.),
causing potential runtime errors if the specified model does not exist.

3. **Inconsistent Goal Checking:** While `create_prompt_manager` seems to verify some conditions, `main` should also
independently validate the 'goal' and 'target' conditions before performing other operations to ensure robustness,
given that checking only at one place could miss logical errors.

4. **Logging without Configuration:** The logging functionality is used, but no logging configuration is set up, meaning
the logs may not appear unless logging has been configured elsewhere, which could be confusing during error resolution.

5. **Empty String Checks:** When retrieving source content, if the file is empty, it could lead to unexpected behavior
or unnecessary API calls. Checking for non-empty content before proceeding would be a safer approach.

6. **Hardcoded Prompt Injection:** The script directly concatenates and formats prompts with user inputs (`goal` and
`target`). While inputs might be constrained, it is always safer to sanitize and validate user inputs to avoid any
chance of unintended behavior.

7. **Exit Status Consistency:** While `sys.exit(1)` indicates an error after certain invalid states, the main function
ends with `sys.exit(0)`, indicating successful execution even when this might not be accurate based on error conditions
encountered earlier. It would be beneficial to ensure consistent exit statuses.

By addressing these defects, such as implementing more comprehensive error handling, ensuring model naming and prompt
formatting are correct, and refining validation logic, the script’s robustness and reliability will be improved.

C:\Users\mtj\codeaid>
```
