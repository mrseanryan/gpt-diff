# gpt-diff
Summarize differences between files or a git diff via an LLM.

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

## Example Run

### Compare a before and after file of C# warnings

```bash
./test.sh
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
