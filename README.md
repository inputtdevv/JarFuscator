# JarFuscator - Inputt.dev

**JarFuscator** is a powerful Java JAR obfuscation tool inspired by Skidfuscator. It encrypts strings, obfuscates classes, renames methods and fields, and supports phantom computations to protect your Java applications.

---

## Features 📚

- **Full JAR obfuscation**: Encrypt strings, obfuscate method/field names, rename classes.
- **Phantom computation**: Protects unused or phantom classes.
- **Library support**: Include external dependencies for obfuscation.
- **Interactive input support**: Prompts for input/output paths if not provided.
- **Randomized output**: Generates random output filenames if not specified.
- **Cleanup**: Removes temporary `.java` and `.class` files after execution.
- **Analytics opt-out**: Optionally skip tracking usage or errors.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/inputtdev/JarFuscator.git
cd JarFuscator
```

2. Install python dependencies.

```bash
py -m pip install colorama
py -m pip install pystyle
```

3. Run The Python file

```bash
python JarFuscation.py {jar} 
```

To list all arguments you can use, type --help when running the script.

Optionally you can install the precompiled .EXE file
