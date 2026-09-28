def test_map():
    thing = map(
        lambda x, y: f"{x}, {y}",
        ["apple", "banana", "pear"],
        ["tomato", "raddish", "dates"]
    )

    print(list(thing))

if __name__ == "__main__":
    test_map()