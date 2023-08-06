# Batch execute any task, with simple json config

This module makes it possible to batch execute almost every program that runs from command line on files in input directory and outputs those into output directory (include directory structure). Settings are taken from config.json file. In the future there will be new features added.

## Installation

```pip install batchexec```

## How to use it?

Import module batchexec, use the class UniversalBatchExecuter from it with the config file (default: 'config.json'):
```batch_executer = batchexec.UniversalBatchExecuter('config.json')```
Then run it with optional additional parameters, e.g.:
```batch_executer.run('--verbose')```

## Parameters in json config file:

```
{
  // Relative or absolute path to input dir. Default: "input"
  "input_dir": "input",
  // Whether to include subdirectories or not. Possible [true, false], Default: true
  "include_subdirs": true,
  // Filter only file masks/extensions to execute apps
  "file_masks": ["*.jpg", "*.jpeg", "*.png", "*.gif"],
  // Relative or absolute path to output dir. If not exists, it will be created. Default: "output"
  "output_dir": "output",
  // Relative or absolute path to own application directory that we want to run. Default: "app"
  "app_dir": "app",
  // Relative path to application executable file that we want to run. Default: "app.exe"
  "app_name": "bin/app.exe",
  // Additional arguments to the application. Default: ""
  "app_args": "-q 75",
  // Parameter after which the input file name is specified. Default: ""
  "app_input_parameter": "-i",
  // Parameter after which the output file name is specified. Default: "-o"
  "app_output_parameter": "-o",
  // When the output file should have specified extension, we can enter it here. Default: "" (extension won't be changed)
  "app_output_file_extension": ".jpg",
  // When the output file already exists, should it be replaced. Possible [true, false], Default: true
  "replace_files": true,
  // When the output file already exists and it will be replaced, should the backup file be created. Possible [true, false], Default: true
  "replaced_files_backup": true,
  // Log output of the application to specified (relative or absolute path to) file. Default: "stdout.log"
  "log_output_to": "stdout.log",
  // Log error output of the application to specified (relative or absolute path to) file. Default: "stderr.log"
  "error_log_output_to": "stderr.log",
}
```

## License

© 2021 Krzysztof Grabowski

This repository is licensed under the MIT license. See LICENSE for details.
