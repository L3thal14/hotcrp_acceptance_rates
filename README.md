# HOTCRP Acceptance Rates extractor

Really shitty way for extracting acceptance rates for different editions of conferences

## Installation and Usage

- ```git clone https://github.com/L3thal14/hotcrp_acceptance_rates```
- ```cd hotcrp_acceptance_rates```
- Install dependencies using ```pip3 install -r requirements.txt```
- Usage: ```python3 hotcrp_extract.py <hotcrp URL>```

**NOTE:** URL should be in the format : `https://<conf/workshop name>.hotcrp.com`. 

**Example:** If the current URL is `https://ccs2022b.hotcrp.com` , then use `https://ccs.hotcrp.com`. 

Try to find the right combination if this does not work for some conferences by hit and trial to see if it shows an error page with past edition links and use that instead.

**TODO:** Shift to printing the table row-wise to view results on the go.


## Example Screenshot

![Example Screenshot](https://github.com/L3thal14/hotcrp_acceptance_rates/blob/master/examples_ss.png)