


def square_helper(num, curr) -> None:

    if num:

        print(str(curr) * (num + curr - 1))
        square_helper(num-1, curr+1)



def square() -> None:

    inpt = int(input())
    square_helper(inpt, 1)



def final_floor_acc(lod, flr) -> int | None:

    if not len(lod):
        return flr
    
    elif flr == 0 and lod[0] == "down":
        print("Invalid")
        return
    
    elif lod[0] == "up":
        return final_floor_acc(lod[1:], flr + 1)
    
    else:
        return final_floor_acc(lod[1:], flr - 1)



def final_floor(lod) -> int | None:
    return final_floor_acc(lod, 0)



def double_odds(l) -> list[int]:

    l = list(filter(lambda x: x % 2, l))
    return list(map(lambda x: x * 2, l))



def main() -> None:

    square()

    print()

    print(final_floor([]))
    print()
    print(final_floor(["up", "up", "down"]))
    print()
    print(final_floor(["down", "up", "up"]))
    print()

    print(double_odds([1, 2, 3, 4, 5, 6]))
    print()
    print(double_odds([2, 4, 4, 2]))
    print()



if __name__ == "__main__":
    main()