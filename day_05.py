

class range_map:
    def __init__(self, lines=None):
        self._dest_arr = []
        self._source_arr = []
        self._duration_arr = []

        if lines is not None:
            for line in lines:
                self._add_range(*[int(x) for x in line.split(' ')])

    def _add_range(self, destination, source, duration):
        self._dest_arr.append(destination)
        self._source_arr.append(source)
        self._duration_arr.append(duration)

    def __getitem__(self, x):
        for dest, source, dur in zip(self._dest_arr, self._source_arr, self._duration_arr):
            if 0 <= x-source <= dur:
                return dest + (x - source)
        return x

    def __call__(self, x):
        return self.__getitem__(x)

    def get(self, x):
        return self.__getitem__(x)

    def __repr__(self):
        return "\n".join([" ".join([str(dest), str(src), str(dur)]) for dest, src, dur in zip(self._dest_arr, self._source_arr, self._duration_arr)])

    def __str__(self):
        return self.__repr__()


class map_composition:
    def __init__(self, *maps):
        self._maps = maps

    def __getitem__(self, x):
        for m in self._maps:
            x = m[x]
        return x

    def __call__(self, x):
        return self.__getitem__(x)

    def get(self, x):
        return self.__getitem__(x)


def load_file(file_name):
    with open(file_name, 'r') as file:
        all_text = file.read().strip()
    segments = all_text.split("\n\n")

    seeds = [int(x) for x in segments[0].lstrip("seeds: ").split(' ')]
    segments = [seg.split('\n')[1:] for seg in segments[1:]]

    # Order
    # seed-to-soil
    # soil-to-fertilizer
    # fertilizer-to-water
    # water-to-light
    # light-to-temperature
    # temperature-to-humidity
    # humidity-to-location

    seed_to_soil = range_map(segments[0])
    soil_to_fert = range_map(segments[1])
    fert_to_water = range_map(segments[2])
    water_to_light = range_map(segments[3])
    light_to_temp = range_map(segments[4])
    temp_to_hum = range_map(segments[5])
    hum_to_loc = range_map(segments[6])

    return seeds, seed_to_soil, soil_to_fert, fert_to_water, water_to_light, light_to_temp, temp_to_hum, hum_to_loc


def main():
    seeds, seed_to_soil, soil_to_fert, fert_to_water, water_to_light, light_to_temp, temp_to_hum, hum_to_loc =  \
        load_file("data/day_05_test.txt")

    all_maps = map_composition(seed_to_soil, soil_to_fert, fert_to_water, water_to_light, light_to_temp, temp_to_hum, hum_to_loc)

    checksum_1 = min((all_maps(x) for x in seeds))
    print(f"Part 1\n{checksum_1}")

    #expanded_seeds = []
    #for s1, s2 in zip(seeds[::2], seeds[1::2]):
    #    expanded_seeds.extend([s1 + x for x in range(s2)])
    #
    #checksum_2 = min((all_maps(x) for x in expanded_seeds))
    #print(f"Part 2\n{checksum_2}")

if __name__ == "__main__":
    main()