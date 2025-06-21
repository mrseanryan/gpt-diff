# gpt-diff

Summarize differences between files or within a git diff, via an LLM.

- Automates the chore of comparing files and writing up a summary.
- Uses a local LLM for maximum privacy.

## Features

- compare 2 files, generate a natural language summary (markdown) of their differences
  - any text file
  - PDF files: can specify a page range
  - alternatively, process a single 'diff' file such as the output of `git diff`
- output in a different langauge
- uses a local LLM (via Ollama) for maximum privacy

The features and quality depend on the LLM model used (tested with Qwen3-8B).

## Setup

1. Install dependencies

```bash
poetry env use 3.12.7
poetry install
```

2. Install a [local LLM](./local_llm/README.md)

## Usage

See the built-in help:

```bash
./go.sh
```

```
Summarize differences between files or within a git diff, via an LLM.

Usage: main_cli.py <before-file> [after-file] [options]

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -e END_PAGE, --end-page=END_PAGE
                        (for PDF file) The End page (1-indexed) to extract
                        text to.
  -l TARGET_LANGUAGE, --language=TARGET_LANGUAGE
                        translate to the target output language
                        TARGET_LANGUAGE. Example: English.
  -o OUTPUT_FILE, --output=OUTPUT_FILE
                        the output file (required). By default is None, so
                        output is to stdout (no file is output).
  -s START_PAGE, --start-page=START_PAGE
                        (for PDF files) The Start page (1-indexed) to extract
                        text from.
  -u USER_PROMPT, --user-prompt=USER_PROMPT
                        additional details to help the LLM perform the diff
                        comparision.
  -v, --verbose         turn on verbose mode
Usage: main_cli.py <before-file> [after-file] [options]
```

## Example Usage

### Compare a before and after file of C# warnings

```bash
echo "Comparing 2 files"
./go.sh ./test_data/csharp-warnings.before.txt   ./test_data/csharp-warnings.after.txt -o temp/csharp-warnings.txt
```

Output:

```
**Summary of Differences Between BEFORE and AFTER Files:**

1. **Removed Warnings:**
   - **CS0168**: "Variable declared but never used" (removed from `src/Models/User.cs`).
   - **CS0219**: "Variable assigned but never used" (removed from `src/Controllers/HomeController.cs`).
   - **CS0162**: "Unreachable code detected" (removed from `src/Utils/StringUtils.cs`).

2. **Added Warnings:**
   - **CS0252**: "Possible unintended reference comparison; use `.Equals` instead" (new in `src/Validation/Comparer.cs`).
   - **CS1573**: "Parameter has no matching `<param>` tag in XML comment" (new in `src/Docs/ApiGenerator.cs`).
   - **CS8619**: "Nullability of reference types in value doesn't match target type" (new in `src/Models/Response.cs`).

3. **Reordered Warnings:**
   - The order of the rows has changed, but the descriptions and file paths for existing warnings (e.g., CS0618, CS0649, CS0108, CS0114, CS1998, CS8618, CS8321) remain the same.

4. **Updated File Paths:**
   - Some warnings now reference new files (e.g., `src/Validation/Comparer.cs`, `src/Docs/ApiGenerator.cs`, `src/Models/Response.cs`), while others retain their original paths (e.g., `src/Services/EmailService.cs`, `src/ViewModels/AccountViewModel.cs`).

**Key Changes:**
The `AFTER` file removes three warnings (CS0168, CS0219, CS0162) and adds three new ones (CS0252, CS1573, CS8619). The descriptions for existing warnings are unchanged, but the file paths for some warnings have shifted, indicating updated or newly introduced code issues.
```

### Compare a before and after file of C# warnings (output in Spanish)

```bash
echo "Comparing 2 files"
./go.sh ./test_data/csharp-warnings.before.txt   ./test_data/csharp-warnings.after.txt -o temp/csharp-warnings.txt -l Spanish
```

Output (Spanish):

```
**Diferencias entre el archivo antes y después:**

1. **Warnings eliminados (no presentes en el "AFTER"):**
   - **CS0168**: "Variable declarada pero nunca usada" (ejemplo: `src/Models/User.cs`).
   - **CS0219**: "Variable asignada pero nunca usada" (ejemplo: `src/Controllers/HomeController.cs`).
   - **CS0162**: "Código inalcanzable detectado" (ejemplo: `src/Utils/StringUtils.cs`).

2. **Warnings agregados (nuevos en el "AFTER"):**
   - **CS0252**: "Comparación de referencia posible por error; usar `.Equals()` en su lugar" (ejemplo: `src/Validation/Comparer.cs`).
   - **CS1573**: "Parámetro no tiene etiqueta `<param>` en comentario XML" (ejemplo: `src/Docs/ApiGenerator.cs`).
   - **CS8619**: "Nullabilidad de tipos de referencia en valor no coincide con el tipo objetivo" (ejemplo: `src/Models/Response.cs`).

3. **Cambios en descripciones o rutas de archivos:**
   - **CS8618**: La ruta de archivo cambió de `src/DTOs/UserDto.cs` a `src/DTOs/UserDto.cs` (no hay cambio).
   - **CS8321**: La descripción y ruta de archivo permanecen igual en ambos archivos.
   - **CS0108 y CS0114**: Descripción y ruta de archivo son idénticas en ambos archivos.

4. **Orden de las filas:**
   - El orden de los warnings en el "AFTER" no sigue la misma secuencia que en el "BEFORE", pero esto no afecta las diferencias mencionadas anteriormente.

**Resumen:**
El "AFTER" elimina tres warnings anteriores (CS0168, CS0219, CS0162) y agrega tres nuevos (CS0252, CS1573, CS8619). Las descripciones y rutas de archivo de los warnings restantes son idénticas en ambos archivos.
```

### More Examples

```bash
echo "Summarizing just 1 git-diff file"
./go.sh ./test_data/csharp-warnings.git-diff.txt -o temp/csharp-warnings.git-diff.txt

echo "Comparing 2 PDF files"
./go.sh  ./temp/overall-report--mcop_1194-system-prompt-tools--run_3_all_after_sean.pdf   ./temp/baseline--overall-report--mcop_1194-system-prompt-tools--run_4_sean_new_baseline.pdf   -o temp/overall-then-baseline.txt  --start-page 1 --end-page 2
```

# Testing

```bash
./test.e2e.sh
```
