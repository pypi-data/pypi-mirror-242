# PokePoke

The PokeAPI is a RESTful API that serves as a comprehensive database for Pokémon-related data. It offers a wide range of information about Pokémon species, their abilities, moves, types, evolutions, and more. By providing endpoints for various queries, such as retrieving details about specific Pokémon or abilities, the PokeAPI allows developers to access and utilize Pokémon-related data in their applications. It serves as a valuable resource for enthusiasts, developers, and researchers interested in integrating Pokémon-related information into their projects.

## API 
Python Basic API wrapper
```http
  https://restcountries.com/v3.1
```

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install countries_info
```

## Usage

```python
from countries import restcountries

def get_user_input():
    country_code = input("Masukkan kode negara (contoh: usa): ")
    return country_code

def main():
    rest_countries_api = restcountries()

    # Mendapatkan input dari pengguna
    country_code = get_user_input()

    # Memanggil fungsi untuk mendapatkan informasi negara berdasarkan kode negara
    country_info = rest_countries_api.get_country_info(country_code)
    
    if "error" in country_info:
        print(country_info["error"])
    else:
        print(f"Informasi Negara untuk {country_code.upper()}:")
        print(country_info)

if __name__ == "__main__":
    main()

```