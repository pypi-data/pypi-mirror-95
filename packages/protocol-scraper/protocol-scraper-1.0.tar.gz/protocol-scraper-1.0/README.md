## Protocol Scraper ⚗️  
### A Python CLI that Automates Protocol Writing.

### Introduction  
This CLI scrapes protocols from [Protocols.io API](https://apidoc.protocols.io/) to automate protocol collection and writing.  
Specify the number of protocols you want to scrape and analyze the generated .txt files to select the best protocol for your needs.  
For obscure protocols it may be required to generate multiple protocols and collate to form the instructions for your needs.  

### Prerequisites:
* Python >=3.6  

### Quick Start:
```
pip install protocol-scraper
```

### Usage:
```
Usage: protocol-scraper [OPTIONS] PROTOCOL

  Arguments:

  PROTOCOL The protocol to write.

Options:
  -l, --limit INTEGER  Number of test protocols to write. Default = 3
  --help               Show this message and exit.
```

### Output:
The CLI will output .txt files containing the scraped protocols to the limit specified.  

**NOTE**: The script will return an error if you try and generate more protocols than there are targets on the site
