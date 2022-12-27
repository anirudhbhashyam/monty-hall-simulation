import argparse
import random
import contextlib


def reveal_door(doors: list[str], choice: int) -> int:
    for i, door in enumerate(doors):
        if door == "🐐" and i != choice:
            return i


def print_doors(goat_position: int = None, win_position: int = None) -> None:
    doors = ["🚪"] * 3

    if goat_position is not None:
        doors[goat_position] = "🐐"
    if win_position is not None:
        doors[win_position] = "🏆"

    for door in doors:
        print(f" {door} ", end = "")


def simulate(manual_choice: int = None, manual_switch: int = None) -> bool:
    won = False
    doors = ["🐐"] * 3

    prize_position = random.randint(0, 2)

    doors[prize_position] = "🏆"

    print("There are three doors in front of you.")
    print("Behind one door is a prize, behind the others, goats.")
    print("Which door do you choose? 1, 2, or 3?")
    print_doors()

    if manual_choice is None:
        choice = input("Enter your choice: ")
        if not choice.isdigit() and 1 <= choice <= 3:
            print("Please enter a number between 1 and 3.")
            return
        choice = int(choice) - 1
    else:
        choice = manual_choice
    
    if choice == prize_position:
        won = True
        print("You win!")
    else:
        revealed_position = reveal_door(doors, choice)
        print(f"The host reveals door {revealed_position + 1} to be a goat.")
        print_doors(goat_position = revealed_position)
        print()
        print("Do you want to switch doors?")

        if manual_switch is None:
            switch = int(input("1 for yes, 2 for no: "))
        else:
            switch = manual_switch

        if switch != 1 and switch != 2:
            print("Please enter 1 or 2.")
            return
        
        if switch == 1:
            choice = 3 - choice - revealed_position
        if choice == prize_position:
            print("You win!")
            won = True
        else:
            print("You lose!")

    return won


def play(n_simulations: int = 10) -> dict[str, float]:
    wins = 0
    switch_wins = 0
    manual_switches = 0
    with contextlib.redirect_stdout(None):
        for _ in range(n_simulations):
            switch = random.randint(1, 2)
            if switch == 1:
                manual_switches += 1
            if simulate(random.randint(1, 3), switch):
                wins += 1
                if switch == 1:
                    switch_wins += 1

    dct = {
        "n_simulations": n_simulations,
        "win rate": round(wins / n_simulations, 4),
        "switch rate": round(manual_switches / n_simulations, 4),
        "switch win rate": round(switch_wins / manual_switches, 4),
        "stay win rate": round((wins - switch_wins) / (n_simulations - manual_switches), 4),
    }

    return dct


def process_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n",
        "--n_simulations",
        type = int,
        default = 10000,
        help = "Number of simulations to run.",
    )
    parser.add_argument(
        "-m",
        "--mode",
        type = str,
        default = "sim",
        help = "Mode to run the program in. 'sim' for simulation, 'play' to play the game.",
    )
    return parser.parse_args()


def main() -> int:
    args = process_args()
    n_simulations = args.n_simulations
    mode = args.mode

    if not str(n_simulations).isdigit():
        print("Please enter a valid number of simulations.")
        return 1
    
    match mode:
        case "sim":
            metrics = play(int(args.n_simulations))
            for metric, value in metrics.items():
                print("".center(30, "-"))
                if metric == "switch win rate":
                    print(f"\033[32m{metric:<20} | {value}\033[0m")
                    continue
                print(f"{metric:<20} | {value}")
        case "play":
            simulate()
        case _:
            print("Please enter a valid mode.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())