# AssistFetch
## Requirements:
Chrome version > 90.0.0

## Setup:
1. Open the project directory
1. `pip install -r requirements.txt`
1. `python3 src/fetch.py <commands> <arguments>` (see explanation and example usage below)

## Command List:
- `--help [-h]`: No argument value is needed, this command will display a help doc to explain the usage for this script
- `--list [-l]`: With this command, the value should be one of the following `year`, `from_school`, `to_school`. The script will then proceed to fetch the available academic years, available schools (from), or available schools (to) in assist.org. Note that if the value is `to_school`, the command `-f` or `--from_school` should also be set since we need to know which school to know the one end of the agreement school in order to get the available other end of schools.
> 
- - - -
- **Note**: The commands below are for fetching the list of majors of a specific year, from a specific school to a specific agreement school, this means in order to successfully fetching a list, all commands will need to be present.
- `--year [-y]`: Specify the academic year to fetch major list, in a form like `"2020-2021"`
- `--from_school [-f]`: Specify the school to fetch available transfer major from, for example `"De Anza College"`
- `--to_school [-t]`: Specify the agreement school to fetch major list from, corresponding to the specified <from_school>, for example `"University of California, Berkeley"`

## Example Usage: 
`python3 src/fetch.py -<option> <value>`
- Getting help: `python3 src/fetch.py -h`
- Getting a list of available years on assist.org: `python3 src/fetch.py --list year`
- Getting a list of agreement schools with De Anza College: `python3 src/fetch.py --list to_school --from_school "De Anza College"`
- Getting a list of transferable majors in school year 2020-2021 from De Anza College to UCLA: `python3 src/fetch.py -y 2020-2021 -f "De Anza College" -t "University of California, Los Angeles"`
 
## Note:
Currently this script only prints the result of the command specified. If you need the result to be routed in other forms (WebSockets, json file, rpc...), feel free to open an issue so I will work on it, or you can open a branch to do it yourself, and submit a PR for us to review and merge it into development.


