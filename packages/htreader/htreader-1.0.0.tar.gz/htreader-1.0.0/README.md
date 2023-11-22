# htreader

Installation

`pip install htreader`

```
from htreader.htreader import (
    ReadText,
    WriteText,
    UpdateText,
    DeleteFiles,
    CreateFiles
)
```

# Usage

To open and read content of files:` ReadText()`

```
from htreader.htreader import ReadText

files = './example.txt'
read = ReadText(files)
print(read)

"""You can try with this::"""
ReadText(file_name = files##)

```

To create a new file and write on it: `CreateFiles()`

```
from htreader.htreader import ReadText, WriteText, UpdateText,DeleteFiles, CreateFiles

files = './example.txt'
use = CreateFiles(
    file_name=files,
    create="this is the content of files"
)

```

To write files:  `WriteText()`

```
from htreader.htreader import ReadText, WriteText

files = './example.txt'

use = WriteText(
    file_name = files, 
    contents = "i am prood of me\n i have knowledge."
)
print(files)
```

To Update files content:` UpdateText()`

```
from htreader.htreader import ReadText, WriteText, UpdateText

files = './example.txt'
text = "\n this is a new text for updated"

use = UpdateText(
    file_name=files,
    update_contents=text
)

print(use)
```

To Delete files: `DeleteFiles()`

```
from htreader.htreader import ReadText, WriteText, UpdateText,DeleteFiles

files = './example.txt'
use = DeleteFiles(file_name=files)
print(use)

```
