# INECrawler
INE Crawler is a tool to extract data from the National Statistics Institute. 

<div id="top"></div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/wake-ua/INECrawler">
    <img src="images/logo.png" alt="Logo" width="200" height="200">
  </a>

  <p align="center">
    A tool to craw data to your projects from open data portals
    <br />
    <a href="https://github.com/wake-ua/INECrawler/issues">Report Bug</a>
    ·
    <a href="https://github.com/wake-ua/INECrawler/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#requirements">requirements</a></li>
      </ul>
    </li>
    <li><a href="#examples">Examples for usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project
INE Crawler is a tool to extract data from the National Statistics Institute.

Features:
* Download datasets from INE portal
* Download metadata from resources
* Filter by year
* Filter by topic (just 'tourism' by the moment)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started
This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Requirements
* You need python 3.9 installed

* Clone the repo
  ```sh
  git clone https://github.com/wake-ua/INECrawler.git
  ```

* Install the requirements from requirements.txt
  ```sh
  pip3 install -r requirements.txt
  ```

<!-- USAGE EXAMPLES -->
### Examples

#### Dowload all metadata from INE portal:
```
python inecrawler
```
#### Dowload all datasets with their metadata:
```
python inecrawler -d
```
#### Dowload specifics categories. Only avilable 'Turismo':
```
python inecrawler -c Turismo
```
#### Dowload specific year. For example 2022:
```
python inecrawler -y 2022
```
#### Dowload specific operation. For example 62:
```
python inecrawler -id 62
```
#### Dowload in a specific path.:
```
python inecrawler -p /my/example/path/
```
#### Help with all posible commands:
```
python inecrawler -h
```
_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#top">back to top</a>)</p>

## INE site

- [x] https://servicios.ine.es

\* Works with restrictions or download limitations

See the [open issues](https://github.com/wake-ua/INECrawler/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->
## License
Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>

## Colaborators
🙋‍♂️Alberto Berenguer Pastor \
📱[@aberenguerpas](https://twitter.com/aberenguerpas) \
✉️ alberto.berenguer@ua.es

<!-- CONTACT -->
## Contact
🙋‍♂️Paula González Martínez \
📱[@lucyleia28](https://www.linkedin.com/in/paulagonzalezmartinez/) \
✉️ pgm136@alu.ua.es

<p align="right">(<a href="#top">back to top</a>)</p>