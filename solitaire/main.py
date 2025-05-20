from solitaire.klondike import Klondike


def main():
    game = Klondike()
    while True:
        game.display()
        cmd = input('Command (draw/move/quit): ').strip().lower()
        if cmd == 'quit':
            break
        if cmd == 'draw':
            game.draw()
            continue
        if cmd.startswith('move'):
            parts = cmd.split()
            if len(parts) >= 3:
                src = parts[1]
                dest = parts[2]
                count = int(parts[3]) if len(parts) >= 4 else 1
                game.move(src, dest, count)
            else:
                print('Usage: move <src> <dest> [count]')
            continue
        print('Unknown command')


if __name__ == '__main__':
    main()
