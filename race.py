from microbit import Image, display, button_a, button_b, sleep
import random


# Delay in microseconds between cycles.
CLOCK = 25

# Initial state of the game.
INIT_GAME = {
    'row': 0,
    'field': [[0] * 5] * 5,
    'pos': 2,
    'delay': 500,
    'time': 0
}

state = ['init']


def get_state(i, default=None):
    if len(state) <= i:
        return default
    return state[i]


def set_state(i, value):
    filler = [None] * 5
    state[:] = (state + filler)[:i] + [value]


while True:
    sleep(CLOCK)

    if get_state(0) == 'init':
        i = get_state(1, 0)
        if i < 500 / CLOCK:
            display.show(Image.HAPPY)
        else:
            display.show(Image.ARROW_W)
        set_state(1, (i + 1) % (1000 / CLOCK))
        if button_a.was_pressed():
            set_state(0, 'game')

    elif get_state(0) == 'game':
        game = get_state(1, INIT_GAME)

        # Check for collisions.
        if game['field'][4][game['pos']]:
            score = game['row']
            set_state(0, 'crashed')
            set_state(1, score)
            button_a.was_pressed()  # Reset the button press flag.
            continue

        # Handle controls.
        if button_a.was_pressed():
            game['pos'] = max(0, game['pos'] - 1)
        if button_b.was_pressed():
            game['pos'] = min(4, game['pos'] + 1)

        # Move the field if needed.
        game['time'] += CLOCK
        if game['time'] > game['delay']:
            game['time'] = 0
            game['row'] += 1
            new_row = [0] * 5
            if game['row'] % 2:
                new_row[random.randint(0, 4)] = 5
            game['field'] = [new_row] + game['field'][:4]
            game['delay'] -= game['delay'] / 50

        # Redraw field
        frame_buffer = [[x for x in row] for row in game['field']]
        frame_buffer[4][game['pos']] = 9
        screen = Image(':'.join(''.join(map(str, row))
                                for row in frame_buffer))
        display.show(screen)

    elif get_state(0) == 'crashed':
        if button_a.was_pressed():
            score = get_state(1)
            set_state(0, 'score')
            set_state(1, score)

    elif get_state(0) == 'score':
        score = get_state(1)
        if score:
            display.scroll('score: {}'.format(score), wait=False, loop=True)
            set_state(1, 0)
        if button_a.was_pressed():
            set_state(0, 'init')
