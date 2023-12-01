# JSONGenerator
 JSON generator from Excel files with template.

### Dependencies
- pandas
- tkinter

## Usage
using template to build up the links between Excel and JSON entries

- Excel column names → match template → JSON path

### Format
formats of the entries in Excel dataset
1. string: ```"example"```
2. int & float: ```15```, ```1.0```
3. range: ```[-1,100]```
4. list: ```l[121,abc,def]```, ```l["anc,"hele",""test"]```
   - string elements only
   - begin with ```l[``` as the notation 
5. dict:
   - no dictionary as entries, instead using column names to locate the position directly.