import requests


def _call(point):
    response = requests.get(
        f"https://tyradex.tech/api/v1/{point}",
        headers={
            "User-Agent": "RobotPokemon",
            'Content-type': 'application/json'
        }
    )

    if response.status_code == 200:
        data = response.json()
        return (data)
    else:
        raise RuntimeError("La requête a échoué avec le code d'état:", response.status_code)


class Pokemon:
    def __init__(self, identifiant: int | str | dict, region: str = ...):
        """ Permet d'obtenir des informations sur un Pokémon spécifique.

        :param identifiant: Correspond à l'identifiant du Pokémon dans le Pokédex National ou son nom.
        :param region: Correspond à la région du Pokémon. Permet de récupèrer les informations sur une forme régionale d'un Pokémon.
        """
        if isinstance(identifiant, dict):
            self.__data = identifiant
        else:
            self.__data = _call(f'pokemon/{identifiant}' + ('' if region is ... else f'/{region}'))

    def __str__(self):
        return self.name.fr

    def __repr__(self):
        return self.pokedex_id

    @property
    def pokedex_id(self) -> int:
        return self.__data['pokedexId']

    @property
    def generation(self) -> int:
        return self.__data['generation']

    @property
    def category(self) -> str:
        return self.__data['category']

    @property
    def name(self):
        return Name(self.__data['name'])

    @property
    def sprites(self):
        return Sprites(self.__data['sprites'])

    @property
    def types(self):
        t = self.__data['types']
        if len(t) == 1:
            return Type(t[0]['name'])
        else:
            return Type(t[0]['name']).put_with(Type(t[1]['name']))

    @property
    def talents(self):
        return [Talent(data) for data in self.__data['talents']]

    @property
    def stats(self):
        return Stats(self.__data['generation'])

    @property
    def resistances(self):
        return [Resistance(data) for data in self.__data['resistances']]

    @property
    def evolution(self):
        return Evolutions(self.__data['evolution'])

    @property
    def height(self) -> float:
        return float(self.__data['height'].replace(',', '.').removesuffix(' m'))

    @property
    def weight(self) -> float:
        return float(self.__data['weight'].replace(',', '.').removesuffix(' kg'))

    @property
    def egg_groups(self) -> list[str]:
        return self.__data['egg_groups']

    @property
    def sexe(self):
        return Sexe(self.__data['sexe'])

    @property
    def catch_rate(self) -> int:
        return self.__data['catch_rate']

    @property
    def level_100(self) -> int:
        return self.__data['level_100']

    @property
    def forme(self):
        return [Forme(data, self.pokedex_id) for data in self.__data['forme']]


class Type:
    class Fusion:
        def __init__(self, type_1: int | str, type_2):
            """ Permet d'obtenir des informations sur un Pokémon spécifique.

            :param type_1: Correspond à l'identifiant du type, ou bien son nom anglais ou français.
            :param type_2: Correspond au deuxième type souhaité. Avec la combinaison, cela vous permet d'obtenir les Pokémons possédants ce double type.
            """
            self.__data = _call(f'types/{type_1}/{type_2}')

        @property
        def id(self) -> list[int]:
            return self.__data['id']

        @property
        def name(self):
            return Name2(self.__data['name'])

        @property
        def sprites(self) -> list[str]:
            return self.__data['sprites']

        @property
        def resistances(self):
            return [Resistance(data) for data in self.__data['resistances']]

        @property
        def pokemons(self):
            class Pokemons:
                def __init__(self, ids):
                    self.ids = ids

                def get(self):
                    return [Pokemon(pokedex_id) for pokedex_id in self.ids]

            return Pokemons([pok['pokedexId'] for pok in self.__data['pokemons']])

    def __init__(self, identifiant: int | str | dict):
        """ Permet d'obtenir des informations sur un Pokémon spécifique.

        :param identifiant: Correspond à l'identifiant du type, ou bien son nom anglais ou français.
        """
        if isinstance(identifiant, dict):
            self.__data = identifiant
        else:
            self.__data = _call(f'types/{identifiant}')

    @property
    def id(self) -> int:
        return self.__data['id']

    @property
    def name(self):
        return Name(self.__data['name'])

    @property
    def sprites(self) -> str:
        return self.__data['sprites']

    @property
    def resistances(self):
        return [Resistance(data) for data in self.__data['resistances']]

    @property
    def pokemons(self):
        class Pokemons:
            def __init__(self, ids):
                self.ids = ids

            def get(self):
                return [Pokemon(pokedex_id) for pokedex_id in self.ids]

        return Pokemons([pok['pokedexId'] for pok in self.__data['pokemons']])

    def put_with(self, other):
        return self.Fusion(self.id, other.id)


class Generations:
    class Gen:
        def __init__(self, generation):
            self.generation = generation
            self._data = [Pokemon(pok['pokedexId']) for pok in _call(f'gen/{generation}')]
            self._data.sort(key=lambda p: p.pokedex_id)

        def __getitem__(self, pokedex_id):
            return self._data[pokedex_id - 1]

        def __iter__(self):
            self.index = 1
            return self

        def __next__(self):
            try:
                obj = self[self.index]
            except IndexError:
                raise StopIteration
            self.index += 1
            return obj

    def __init__(self):
        self._data = [self.Gen(gen['generation']) for gen in _call(f'gen')]
        self._data.sort(key=lambda x: x.generation)

    def __getitem__(self, gen):
        return self._data[gen - 1]

    def __iter__(self):
        self.index = 1
        return self

    def __next__(self):
        try:
            obj = self[self.index]
        except IndexError:
            raise StopIteration
        self.index += 1
        return obj


# =-=-=-=-=-=-=-=-=-=-=-=-=

class Name:
    def __init__(self, __data: dict):
        self.fr: str = __data["fr"]
        self.en: str = __data["en"]
        self.jp: str = __data["jp"]

    def __str__(self):
        return self.fr


class Name2:
    def __init__(self, __data: dict):
        self.fr: list[str] = __data["fr"]
        self.en: list[str] = __data["en"]
        self.jp: list[str] = __data["jp"]

    def __str__(self):
        return ', '.join(self.fr)


class Talent:
    def __init__(self, __data):
        self.name: str = __data['name']
        self.talent_cache: bool = __data['tc']


class Sprites:
    def __init__(self, __data):
        self.regular: str = __data['regular']
        self.shiny: str = __data['shiny']
        self.gmax: str = __data['gmax']


class Stats:
    def __init__(self, __data):
        self.hp_: int = __data["hp"]
        self.atk_: int = __data["atk"]
        self.def_: int = __data["def"]
        self.spe_atk_: int = __data["spe_atk"]
        self.spe_def_: int = __data["spe_def"]
        self.vit_: int = __data["vit"]


class Resistance:
    def __init__(self, __data):
        self.name: str = __data['name']
        self.multiplier: float = __data['multiplier']


class Evolutions:
    def __init__(self, __data):
        self.pre: list = [Evolution(data) for data in __data['pre']] if __data['pre'] is not None else []
        self.next: list = [Evolution(data) for data in __data['next']] if __data['next'] is not None else []
        self.mega: list = [Evolution(data) for data in __data['mega']] if __data['mega'] is not None else []


class Evolution:
    def __init__(self, __data):
        self.pokedex_id: int = __data['pokedexId']
        self.name: str = __data['name']
        self.condition: str = __data['condition']

    def get(self):
        return Pokemon(self.pokedex_id)


class Sexe:
    def __init__(self, __data):
        self.male: int = __data['male']
        self.female: int = __data['female']


class Forme:
    def __init__(self, __data, pokedex_id):
        self.region = list(__data.keys())[0]
        self.name = list(__data.values())[0]

        self.get = lambda: Pokemon(pokedex_id, region=self.region)


# =-=-=-=-=-=-=-=-=-=-=-=-=

def get_all_pokemons():
    """ Permet d'obtenir la liste de tous les Pokémons.

    :return: La liste de tous les Pokémons.
    """
    return [Pokemon(data) for data in _call('pokemon')]


def get_all_types():
    """ Permet d'obtenir la liste de tous les Types.

    :return: La liste de tous les Types.
    """
    return [Type(data) for data in _call('types')]
