setup
```bash
    python generateTable.py
    g++ -O3 -Wall -shared -std=c++11 -fPIC $(python3 -m pybind11 --includes) heuristic_module.cpp -o heuristicGenerateMove$(python3-config --extension-suffix)
```

run
```bash
    python main.py path/to/folder_with_fast5_files
```

[more info](https://misqo.github.io/)