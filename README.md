# Migratory Data Assessment Tool

The Migratory Data Assessment Tool is a Python script that analyzes tracked data files to calculate various parameters and generate insightful statistics. This tool is designed to process CSV files containing tracked data of cell movement.

## Requirements

- Python 3.6 or higher
- Pandas library
- Numpy library

## Usage

1. Place the input CSV files in the `input_files` directory.
2. Run the `main.py` script.

```shell
python main.py
```

3. The script will process the input files and generate an output file in the `output_files` directory. The output file will be named with the current timestamp.

## Output

The output file will contain the following information:

- For each input file:
  - Xf-Xi values for all tracks.
  - Tactic index calculated based on Xf-Xi values.
  - Individual track values:
    - Track number.
    - Xf-Xi value.
    - Average positive step displacement.
    - Average negative step displacement.
    - Velocity.
    - Velocity change.
    - Track length.

- Average values for all input files:
  - Number of Positive Cells: Count of cells with positive displacements.
  - Number of Negative Cells: Count of cells with negative displacements.
  - Average +ve Step Displacement (Positive DX): Average positive step displacement for cells with positive displacements.
  - Average -ve Step Displacement (Positive DX): Average negative step displacement for cells with positive displacements.
  - Average +ve Step Displacement (Negative DX): Average positive step displacement for cells with negative displacements.
  - Average -ve Step Displacement (Negative DX): Average negative step displacement for cells with negative displacements.
  - Average +ve Velocity: Average velocity for cells with positive displacements.
  - Average -ve Velocity: Average velocity for cells with negative displacements.
  - Average +ve Velocity Change: Average velocity change for cells with positive displacements.
  - Average -ve Velocity Change: Average velocity change for cells with negative displacements.
  - Average +ve Track Length: Average track length for cells with positive displacements.
  - Average -ve Track Length: Average track length for cells with negative displacements.

## File Structure

```
.
├── main.py
├── input_files/
│   ├── data_file1.csv
│   ├── data_file2.csv
│   └── ...
└── output_files/
    ├── YYYY-MM-DD_HH-MM-SS.txt
    └── ...
```

- `main.py`: Python script to run the migratory data assessment tool.
- `input_files/`: Directory to place input CSV files.
- `output_files/`: Directory to store the output text files.

## Contributing

Contributions to the Migratory Data Assessment Tool are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
