import flet as ft
from enum import Enum
import asyncio

class MovementDirection(str, Enum):
    """game character possible movement directions"""

    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"
    IDLE = "idle"

def main(page: ft.Page):
    game_icon_size = 50
    speed = 5
    speed_label = ft.Text(f"Speed: {speed}")
    snorlax_width = 160
    snorlax_height = 124
    snorlax = ft.Container(
        content = ft.Image(src="pngegg.png", width=snorlax_width, height= snorlax_height), 
        left=110, 
        top=170,
        )
    
    game_area = ft.Stack(
        controls=[snorlax],
        expand=True,
        height = 400,
    )

    state: dict[str, any] = {"speed": speed, "direction": MovementDirection.IDLE}

    def handle_movement(direction: MovementDirection) -> None:
        match direction:
            case MovementDirection.LEFT:
                move_left()
            case MovementDirection.RIGHT:
                move_right()
            case MovementDirection.UP:
                move_up()
            case MovementDirection.DOWN:
                move_down()
            case MovementDirection.IDLE:
                pass

    def on_speed_change(e):
        state["speed"] = int(e.control.value)
        speed_label.value = f"Speed: {state['speed']}"
        page.update()

    speed_slider = ft.Slider(
        min=2,
        max=20,
        divisions=18,
        value=speed,
        label="{value}",
        on_change=on_speed_change,
    )

    movement_status = ft.Text("Stay in bounds")

    def move_left():
        if snorlax.left - state["speed"] >= 0 + 12:
            snorlax.left -= state["speed"]
            movement_status.value = "moving left"
        else:
            movement_status.value = "hit left boundary"

    def move_right():
        max_width = game_area.width if game_area.width else 800
        if snorlax.left + state["speed"] <= max_width - snorlax_width - 16:
            snorlax.left += state["speed"]
            movement_status.value = "moving right"
        else:
            movement_status.value = "hit right boundary"

    def move_up():
        if snorlax.top - state["speed"] >= 0:
            snorlax.top -= state["speed"]
            movement_status.value = "moving up"
        else:
            movement_status.value = "hit top boundary"

    def move_down():
        if snorlax.top + state["speed"] <= game_area.height - snorlax_height + 90:
            snorlax.top += state["speed"]
            movement_status.value = "moving down"
        else:
            movement_status.value = "hit bottom boundary"

    left_button = ft.IconButton(
        icon=ft.Icons.ARROW_LEFT, 
        icon_size=game_icon_size, 
        on_click=lambda e: state.update({"direction": MovementDirection.LEFT}), 
        bgcolor = "green",
    )
    right_button = ft.IconButton(
        icon=ft.Icons.ARROW_RIGHT, 
        icon_size=game_icon_size, 
        on_click=lambda e: state.update({"direction": MovementDirection.RIGHT}), 
        bgcolor = "red",
    )
    up_button = ft.IconButton(
        icon=ft.Icons.ARROW_DROP_UP, 
        icon_size=game_icon_size, 
        on_click=lambda e: state.update({"direction": MovementDirection.UP}), 
        bgcolor = "blue",
    )
    down_button = ft.IconButton(
        icon=ft.Icons.ARROW_DROP_DOWN, 
        icon_size=game_icon_size, 
        on_click=lambda e: state.update({"direction": MovementDirection.DOWN}), 
        bgcolor = "yellow",
    )

    game_controller = ft.Row(
        [left_button, right_button, up_button, down_button],
        alignment = ft.MainAxisAlignment.CENTER,
    )

    async def game_loop():
        while True:
            handle_movement(state["direction"])
            page.update()
            await asyncio.sleep(0.1)

    project_title = ft.Text(
        "Python Async Communication", size=40, weight=ft.FontWeight.BOLD
    )

    author_name = ft.Text(
        "Developed by Aryhanna Pham, University of California, San Diego",
        size=30, 
        weight=ft.FontWeight.BOLD,
    )

    description = ft.Text(
        "During intern interview, ask me about: "
        + "asyncio, asynchronous function, lambda, while loop"
        + "conditionals - if/else, match/case, boolean logic, lists" 
        + "enum, docker, serverless cloud deploy, GitHub, git",
        size=20,
    )

    page.run_task(game_loop)

    page.add(
        project_title,
        author_name,
        description,
        game_controller, 
        ft.Row(
            [
                speed_label, 
                speed_slider,
                movement_status,
            ]
        ),
        game_area
    )

#if __name__ == "__main__":
#    ft.run(main, assets_dir="assets")

app = ft.app(target=main, assets_dir="assets", export_asgi_app=True)