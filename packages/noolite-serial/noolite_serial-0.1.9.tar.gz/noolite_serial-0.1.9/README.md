## Noolite MTRF-64
Поддержка приема и отправки команд noolite mtrf-64 в асинхронном режиме

Все команды шлются с гарантией очередности. Новые команды не отправляются без ответа об отправке предыдущих
```python
from noolite_serial import Noolite, NooliteCommand, const
import asyncio

loop = asyncio.get_event_loop()
noo = Noolite('/dev/serial0', loop=loop)

async def test():
    # отправка команды вкл на канал 1
    await noo.send_command(NooliteCommand(ch=1, cmd=const.ON))
    # отправка яркости
    await noo.send_command(NooliteCommand.make_command(
        ch=1, 
        cmd=const.SET_BRIGHTNESS,
        br=10
    ))
    # отправка временного включения
    await noo.send_command(NooliteCommand.make_command(
        ch=1, 
        cmd=const.TEMPORARY_ON,
        duration=10
    ))

    
# регистрация колбэка на входящие команды
@noo.callback(4)
async def callback(cmd: NooliteCommand):
    print(cmd)

```