### TL;DR

**Undupify** allows to get rid of most of irrelevant and identical-in-behavior URLs in a file. **Undupify** incorporates itself really well in a hacking workflow where you would want to apply a second layer of filtering to your URLs before sending them to a deep time-consuming vulnerability scan.

---

### Demo

![Mask group](https://user-images.githubusercontent.com/52637916/157899499-bb835dab-7832-4174-a577-d7ce508b5c1a.png)

---

### Description

When searching vulnerabilities at scale, it is a very frequent practice to retrieve all URLs associated to a company, with tools such as *waybackurls* or *gau*, and then perform query-parameters-based filtering, looking for XSS, SQLi, SSRF, etc.

In this context, even though retrieved URLs have been processed by a first layer of filtering, a bunch of URLs would stil remain, and lots of them would be completely irrelevant by basically consisting of a subtle variations of others. 
Even though they would have some different path names or different parameters’s value, they would be processed by the exact same back-end function. When this happens, we of course don’t want to deal with them multiple times, as they would basically have the same behavior against fuzzing.

This is where **Undupif**y becomes useful : based on heuristics, it attempts to efficiently distinguish which URLs are duplicates of others, and remove them.

To detect whether an analyzed URL is duplicate or unique, the tool currently relies on the two following heuristics : 

- Heuristic 1  - If the analyzed URL has the exact same paths and parameters, but not necessarily same parameters’ values, as a previously seen URL, then it should be considered duplicate.
- Heuristic 2 - If the analyzed URL has the exact same content between its two first path, delimited by `/`, and the same parameters as a previously seen URL, then it should be considered duplicate.

---

### Usage

```
python3 undupify.py -h
```

This displays help for the tool.

```
usage: undupify.py [-h] [--file FILE] [--output]

options:
  -h, --help            show this help message and exit
  --file FILE, -f FILE  file containing all URLs to clean
  --output, -o          output file path
```

Basic use: 

```
python3 undupify.py -f URLs_to_filter.txt
```
---

### Installation

1 - Clone 

```
git clone https://github.com/Th0h0/undupify.git
```

2  - Install requirements

```
cd autoredirect 
pip install regex
```

---

### License

**Undupify** is distributed under [MIT License](https://github.com/Th0h0/undupify/blob/master/LICENSE.md).
