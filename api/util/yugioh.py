
def render_card_in_console(card_name, card_value):
    # format a 3d card using astrixs * and have the card name in the middle
    # print the card to the console
    for i in range(5):
        print("*" * 10)
    print(f"**{card_name}**")
    print(f"**{card_value}**")
    for i in range(5):
        print("*" * 10)

    return card_name, card_value
        