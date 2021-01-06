import asyncio
from time import sleep
from typing import List

# import httpx
from django.http import HttpResponse


# TODO async https://webdevblog.ru/asinhronnye-predstavleniya-v-django-3-1/
# TODO classbase https://medium.com/@bruno.fosados/django-async-class-based-views-acbv-5986c4511ae6

async def http_call_async():
    for num in range(1, 6):
        await asyncio.sleep(1)
        print(num)
    # async with httpx.AsyncClient() as client:
    #     r = await client.get("https://httpbin.org/")
    #     print(r)


async def smoke(smokables: List[str] = None, flavor: str = "Sweet Baby Ray's") -> None:
    """ Smokes some meats and applies the Sweet Baby Ray's """
    if smokables is None:
        smokables = [
            "ribs",
            "brisket",
            "lemon chicken",
            "salmon",
            "bison sirloin",
            "sausage",
        ]
    if (loved_smokable := smokables[0]) == "ribs":
        loved_smokable = "meats"
    for smokable in smokables:
        print(f"Smoking some {smokable}....")
        await asyncio.sleep(1)
        sleep(4)
        print(f"Applying the {flavor}....")
        await asyncio.sleep(1)
        print(f"{smokable.capitalize()} smoked.")
    print(f"Who doesn't love smoked {loved_smokable}?")


# views

async def index(request):
    return HttpResponse("Hello, async Django!")


async def async_view(request):
    loop = asyncio.get_event_loop()
    loop.create_task(http_call_async())
    return HttpResponse("Non-blocking HTTP request")


async def smoke_some_meats(request) -> HttpResponse:
    loop = asyncio.get_event_loop()
    smoke_args = []
    if to_smoke := request.GET.get("to_smoke"):
        # Grab smokables
        to_smoke = to_smoke.split(",")
        smoke_args += [[smokable.lower().strip() for smokable in to_smoke]]
        # Do some string prettification
        if (smoke_list_len := len(to_smoke)) == 2:
            to_smoke = " and ".join(to_smoke)
        elif smoke_list_len > 2:
            to_smoke[-1] = f"and {to_smoke[-1]}"
            to_smoke = ", ".join(to_smoke)
    else:
        to_smoke = "meats"
    if flavor := request.GET.get("flavor"):
        smoke_args.append(flavor)
    loop.create_task(smoke(*smoke_args))

    return HttpResponse(f"Smoking some {to_smoke}....")
