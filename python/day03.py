from typing import List

from day import Day


class Day03(Day):
    @property
    def day_name(self) -> str:
        return "03"

    def star1(self, lines: List[int]) -> str:
        number_len = len(lines[0])
        bit_set_counts = [0] * number_len
        for line in lines:
            for idx, c in enumerate(line):
                if c == "1":
                    bit_set_counts[idx] += 1
        threshold = len(lines) // 2
        gamma_rate = 0
        epsilon_rate = 0
        two_power = 2 ** (number_len - 1)
        for bit_count in bit_set_counts:
            if bit_count >= threshold:
                gamma_rate += two_power
            else:
                epsilon_rate += two_power
            two_power //= 2
        return str(gamma_rate * epsilon_rate)

    def progressive_filtering(self, numbers: List[str], oxygen_mode: bool) -> int:
        active_numbers = numbers
        for pos in range(len(numbers[0])):
            count_bit_set = sum([int(n[pos]) for n in active_numbers])
            threshold = (len(active_numbers) + 1) // 2
            if (oxygen_mode and count_bit_set >= threshold) or (
                not oxygen_mode and count_bit_set < threshold
            ):
                selected_bit = "1"
            else:
                selected_bit = "0"
            active_numbers = [n for n in active_numbers if n[pos] == selected_bit]
            if len(active_numbers) == 1:
                return int(active_numbers[0], 2)

        raise Exception("More thn one number remaining!")

    def star2(self, lines: List[int]) -> str:
        oxygen_rating = self.progressive_filtering(lines, True)
        co2_rating = self.progressive_filtering(lines, False)
        return str(oxygen_rating * co2_rating)


if __name__ == "__main__":
    Day03().main()
