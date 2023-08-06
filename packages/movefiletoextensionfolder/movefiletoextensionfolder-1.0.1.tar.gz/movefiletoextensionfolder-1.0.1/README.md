# Move files from source Folder to provided destination folder 
It will organise all files in source folder according to the extenstion
of file,
like all jpg will be in one folder all pdf will in one folder.

## Installation

```pip install movefiletoextensionfolder```

## How to use it?
```
from movefiletoextensionfolder import movefile as mf

source_folder_path = r'C:\Users\bhask\Downloads' + '\\'
target_folder_path = r'C:\Users\bhask\Downloads'
successvoicemsg="Hi Bhaskar all files moved Succesfully" 

mf.movefilefromsourcetodestination(source_folder_path,target_folder_path,successvoicemsg)
```

## License

© 2021 kumar bhaskar

This repository is licensed under the MIT license. See LICENSE for details.
