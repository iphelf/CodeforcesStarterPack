# Monorepo for programming practices

## Usage

![Demo](doc/demo.png)

### Coding

Code under `source` directory.

Test your code against the test case (`in.txt` and `oracle.txt`) with CTest:

```
ctest --output-on-failure
```

or, use `tool/tester.py` directly:

```
./tool/tester.py <executable> <input file> <oracle file>
```

### Managing

Manage your code with this directory structure:

- `source`: current working code
- `template`: template code
- `archive`: history code

And use `tool/archiver.py` to automate operations:

```shell
# To backup `source` to `archive`:
./tool/archiver.py backup

# To restore from some directory under `archive`:
./tool/archiver.py restore

# To reset `source` with `template`
./tool/archiver.py reset

# To backup `source` to `archive` and then reset `source` with `template`
./tool/archiver.py archive
```

Note: use `archiver.ini` or command line arguments to specify paths.