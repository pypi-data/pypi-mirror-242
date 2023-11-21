import fourmi

colors = fourmi.colors

def send(text, color='\033[0m', bold=False, italics=False, underline=False, bg_color=None, invert=False):
    rgb = fourmi.colors.get(color)
    if rgb:
        r, g, b = rgb.red, rgb.green, rgb.blue
        ansi_color = f"\033[38;2;{r};{g};{b}m"
        styles = []


        if bold:
            styles.append('1')
        if italics:
            styles.append('3')
        if underline:
            styles.append('4')
        if invert:
            styles.append('7')

        if styles:
            ansi_styles = ';'.join(styles)
            ansi_color += f"\033[{ansi_styles}m"

        if bg_color:
            bg_rgb = fourmi.colors.get(bg_color)
            if bg_rgb:
                bg_r, bg_g, bg_b = bg_rgb.red, bg_rgb.green, bg_rgb.blue
                ansi_color += f"\033[48;2;{bg_r};{bg_g};{bg_b}m"
            else:
                ansi_color += "\033[49m"

        print(f"{ansi_color}{text}\033[0m")
    else:
        ansi_color = f"\033[38m"
        styles = []

        if bold:
            styles.append('1')
        if italics:
            styles.append('3')
        if underline:
            styles.append('4')
        if invert:
            styles.append('7')

        if styles:
            ansi_styles = ';'.join(styles)
            ansi_color += f"\033[{ansi_styles}m"

        if bg_color:
            bg_rgb = colors.get(bg_color)
            if bg_rgb:
                bg_r, bg_g, bg_b = bg_rgb.red, bg_rgb.green, bg_rgb.blue
                ansi_color += f"\033[48;2;{bg_r};{bg_g};{bg_b}m"
            else:
                ansi_color += "\033[49m"
        print(f"{ansi_color}{text}\033[0m")