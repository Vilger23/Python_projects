class Color:
	black = (25, 25, 25)
	white = (240, 230, 230)
	gray = (120, 120, 120)

	blue = (100, 100, 200)
	red = (200, 100, 100)
	green = (100, 200, 100)

def hex(RGB):
	R, G, B = RGB
	f'#{R:02x}{G:02x}{B:02x}'