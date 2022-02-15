import eel
import asyncio
import champselect.websockets as websockets


@eel.expose
def rune_generator():
    print("owo")
    asyncio.run(websockets.main())


# eel init
eel.init('utils/ui', allowed_extensions=['.js', '.html'])
eel.start('main.html', size=(600, 600))
