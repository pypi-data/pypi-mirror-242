# Produce data

```
python eval_qlassical_multitasking.py -d -t {tel} -l {loc} -n {num_runs}
```

where
- `-d` indicates that data should be written to a file
- `-n` is the number runs per produced data point
- `-t` is the number of teleportation programs
- `-l` is the number of local programs

To produce the data for the plot, run:

```
python eval_quantum_multitasking.py -d -t {tel} -l {loc} -n 200
```

**for each combintation of tel and loc from 1 to 15**.

This produces the folders:
```
data/sweep_teleport_local_{tel}_{loc}/
```
**for each combination of tel and loc**.

In each folder, a single simulation run (single run of the python script) produces one `.json` file, with the timestamp of running it as the filename.
Also the `LAST.json` file is always a copy of the most recently created data file.


## Bash script
The `run_{begin}_{end}.sh` scripts may be used to speed up the simulation, by running the simulations for the different combinations of tel and loc in parallel.
They are split in separate ranges such that a single script run does not use up too much memory and CPU.


# Produce plot
Given that the folders `data/sweep_teleport_local_{tel}_{loc}/` exist, a plot can be created with

```
python plot_quantum_multitasking.py -t {tel} -l {loc}
```

where `tel` and `loc` specify the range of data files to use and plot.

For example, when using `-t 3 -l 3`, the data files from
```
data/sweep_teleport_local_1_1/
data/sweep_teleport_local_1_2/
data/sweep_teleport_local_1_3/
data/sweep_teleport_local_2_1/
data/sweep_teleport_local_2_2/
data/sweep_teleport_local_2_3/
data/sweep_teleport_local_3_1/
data/sweep_teleport_local_3_2/
data/sweep_teleport_local_3_3/
```
are used, and a 3x3 heatmap is created.

This produces four files:

```
plots/{timestamp}_tel.png
plots/{timetsamp}_tel_meta.json
plots/{timestamp}_loc.png
plots/{timetsamp}_loc_meta.json
```

These are the plot in `.png` format and a `_meta.json` file with information about which data files were used to procude the plot.
The `tel` files are for the heatmap displaying the teleportation success probability.
The `loc` files are for the heatmap displaying the local program success probability.
All files have the timestamp of generating the plot in the filename. The `LAST_meta.json` and `LAST.png` files are copies of the most recent plot files.

To produce the full 15x15 heatmap, use `python plot_quantum_multitasking.py -t 15 -l 15`.