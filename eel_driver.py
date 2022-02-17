import eel
import asyncio
import champ_identifier


@eel.expose
def rune_generator():
    print("owo")
    text = asyncio.run(champ_identifier.main())
    return text


# eel init
eel.init('utils/ui', allowed_extensions=['.js', '.html'])
eel.start('main.html', size=(1000, 600))
